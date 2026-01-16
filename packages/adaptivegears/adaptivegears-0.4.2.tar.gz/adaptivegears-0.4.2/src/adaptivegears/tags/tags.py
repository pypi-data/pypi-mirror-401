"""Tag fetching and setting with service-specific API support."""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable

import boto3
from rich.progress import track


@dataclass
class TagChange:
    """Represents a tag change to apply to a resource."""

    arn: str
    resource_type: str
    tags_to_set: dict[str, str]


@dataclass
class SetTagsResult:
    """Result of applying tag changes."""

    success: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)  # ARN -> error message


def get_tags_standard(arns: list[str], batch_size: int = 100) -> dict[str, dict]:
    """Fetch tags via ResourceGroupsTaggingAPI (batch of 100)."""
    if not arns:
        return {}

    client = boto3.client("resourcegroupstaggingapi")
    tags = {}
    batches = list(range(0, len(arns), batch_size))

    for start in track(batches, description="Fetching tags (standard)..."):
        batch = arns[start : start + batch_size]
        response = client.get_resources(ResourceARNList=batch)
        for r in response["ResourceTagMappingList"]:
            tags[r["ResourceARN"]] = {t["Key"]: t["Value"] for t in r.get("Tags", [])}

    return tags


def get_tags_iam(arns: list[str]) -> dict[str, dict]:
    """Fetch tags for IAM resources via dedicated API.

    - iam:ListRoleTags for roles
    - iam:ListUserTags for users
    """
    if not arns:
        return {}

    client = boto3.client("iam")
    tags = {}

    for arn in track(arns, description="Fetching tags (IAM)..."):
        # arn:aws:iam::123456789012:role/MyRole
        # arn:aws:iam::123456789012:user/MyUser
        parts = arn.split(":")
        if len(parts) < 6:
            continue

        resource = parts[5]  # role/MyRole or role/path/MyRole
        if "/" not in resource:
            continue

        # IAM resources can have paths: role/service-role/MyRole
        # API wants just the name (last segment), not the path
        resource_parts = resource.split("/")
        resource_type = resource_parts[0]  # "role" or "user"
        resource_name = resource_parts[-1]  # actual name (last segment)

        try:
            if resource_type == "role":
                response = client.list_role_tags(RoleName=resource_name)
                tags[arn] = {t["Key"]: t["Value"] for t in response.get("Tags", [])}
            elif resource_type == "user":
                response = client.list_user_tags(UserName=resource_name)
                tags[arn] = {t["Key"]: t["Value"] for t in response.get("Tags", [])}
        except client.exceptions.NoSuchEntityException:
            # Resource was deleted between listing and tag fetch
            pass

    return tags


def get_tags_wafv2(arns: list[str]) -> dict[str, dict]:
    """Fetch tags for WAFv2 resources via dedicated API.

    - wafv2:ListTagsForResource
    """
    if not arns:
        return {}

    client = boto3.client("wafv2")
    tags = {}

    for arn in track(arns, description="Fetching tags (WAFv2)..."):
        try:
            response = client.list_tags_for_resource(ResourceARN=arn)
            tag_list = response.get("TagInfoForResource", {}).get("TagList", [])
            tags[arn] = {t["Key"]: t["Value"] for t in tag_list}
        except client.exceptions.WAFNonexistentItemException:
            # Resource was deleted between listing and tag fetch
            pass

    return tags


def get_tags_autoscaling(arns: list[str]) -> dict[str, dict]:
    """Fetch tags for Auto Scaling Groups via dedicated API.

    - autoscaling:DescribeTags
    """
    if not arns:
        return {}

    client = boto3.client("autoscaling")
    tags = {}

    # Extract ASG names from ARNs
    # arn:aws:autoscaling:region:account:autoScalingGroup:uuid:autoScalingGroupName/name
    asg_names = []
    arn_to_name = {}
    for arn in arns:
        parts = arn.split(":")
        if len(parts) >= 8:
            # Last part is autoScalingGroupName/actual-name
            name_part = parts[7]
            if name_part.startswith("autoScalingGroupName/"):
                name = name_part.split("/", 1)[1]
                asg_names.append(name)
                arn_to_name[arn] = name

    if not asg_names:
        return {}

    # Fetch tags for all ASGs (API returns tags for all matching filters)
    paginator = client.get_paginator("describe_tags")
    name_to_tags: dict[str, dict] = defaultdict(dict)

    for page in paginator.paginate(
        Filters=[{"Name": "auto-scaling-group", "Values": asg_names}]
    ):
        for tag in page["Tags"]:
            asg_name = tag["ResourceId"]
            name_to_tags[asg_name][tag["Key"]] = tag["Value"]

    # Map back to ARNs
    for arn, name in arn_to_name.items():
        tags[arn] = name_to_tags.get(name, {})

    return tags


# =============================================================================
# Tag Setters
# =============================================================================


def set_tags_standard(arn_to_tags: dict[str, dict[str, str]]) -> dict[str, bool]:
    """Set tags via ResourceGroupsTaggingAPI.

    Note: tag_resources applies same tags to all ARNs in batch,
    so we call per-resource for flexibility.
    """
    if not arn_to_tags:
        return {}

    client = boto3.client("resourcegroupstaggingapi")
    results = {}

    for arn, tags_dict in track(
        arn_to_tags.items(), description="Setting tags (standard)..."
    ):
        try:
            client.tag_resources(
                ResourceARNList=[arn],
                Tags=tags_dict,
            )
            results[arn] = True
        except Exception:
            results[arn] = False

    return results


def set_tags_iam(arn_to_tags: dict[str, dict[str, str]]) -> dict[str, bool]:
    """Set tags for IAM resources via dedicated API.

    - iam:TagRole
    - iam:TagUser
    """
    if not arn_to_tags:
        return {}

    client = boto3.client("iam")
    results = {}

    for arn, tags_dict in track(
        arn_to_tags.items(), description="Setting tags (IAM)..."
    ):
        parts = arn.split(":")
        if len(parts) < 6:
            results[arn] = False
            continue

        resource = parts[5]
        if "/" not in resource:
            results[arn] = False
            continue

        resource_parts = resource.split("/")
        resource_type = resource_parts[0]
        resource_name = resource_parts[-1]

        tags_list = [{"Key": k, "Value": v} for k, v in tags_dict.items()]

        try:
            if resource_type == "role":
                client.tag_role(RoleName=resource_name, Tags=tags_list)
                results[arn] = True
            elif resource_type == "user":
                client.tag_user(UserName=resource_name, Tags=tags_list)
                results[arn] = True
            else:
                results[arn] = False
        except Exception:
            results[arn] = False

    return results


def set_tags_wafv2(arn_to_tags: dict[str, dict[str, str]]) -> dict[str, bool]:
    """Set tags for WAFv2 resources via wafv2:TagResource."""
    if not arn_to_tags:
        return {}

    client = boto3.client("wafv2")
    results = {}

    for arn, tags_dict in track(
        arn_to_tags.items(), description="Setting tags (WAFv2)..."
    ):
        tags_list = [{"Key": k, "Value": v} for k, v in tags_dict.items()]

        try:
            client.tag_resource(ResourceARN=arn, Tags=tags_list)
            results[arn] = True
        except Exception:
            results[arn] = False

    return results


def set_tags_autoscaling(arn_to_tags: dict[str, dict[str, str]]) -> dict[str, bool]:
    """Set tags for Auto Scaling Groups via autoscaling:CreateOrUpdateTags."""
    if not arn_to_tags:
        return {}

    client = boto3.client("autoscaling")
    results = {}

    for arn, tags_dict in track(
        arn_to_tags.items(), description="Setting tags (ASG)..."
    ):
        # Extract ASG name from ARN
        parts = arn.split(":")
        if len(parts) < 8:
            results[arn] = False
            continue

        name_part = parts[7]
        if not name_part.startswith("autoScalingGroupName/"):
            results[arn] = False
            continue

        asg_name = name_part.split("/", 1)[1]

        tags_list = [
            {
                "ResourceId": asg_name,
                "ResourceType": "auto-scaling-group",
                "Key": k,
                "Value": v,
                "PropagateAtLaunch": True,
            }
            for k, v in tags_dict.items()
        ]

        try:
            client.create_or_update_tags(Tags=tags_list)
            results[arn] = True
        except Exception:
            results[arn] = False

    return results


# Fetcher type alias
Fetcher = Callable[[list[str]], dict[str, dict]]

# Map resource_type -> fetcher (default is standard via ResourceGroupsTaggingAPI)
RESOURCE_TAG_GETTERS: dict[str, Fetcher] = {
    "iam:role": get_tags_iam,
    "iam:user": get_tags_iam,
    "wafv2:ipset": get_tags_wafv2,
    "wafv2:rulegroup": get_tags_wafv2,
    "wafv2:webacl": get_tags_wafv2,
    "autoscaling:autoScalingGroup": get_tags_autoscaling,
}

# Setter type alias
Setter = Callable[[dict[str, dict[str, str]]], dict[str, bool]]

# Map resource_type -> setter (default is standard via ResourceGroupsTaggingAPI)
RESOURCE_TAG_SETTERS: dict[str, Setter] = {
    "iam:role": set_tags_iam,
    "iam:user": set_tags_iam,
    "wafv2:ipset": set_tags_wafv2,
    "wafv2:rulegroup": set_tags_wafv2,
    "wafv2:webacl": set_tags_wafv2,
    "autoscaling:autoScalingGroup": set_tags_autoscaling,
}


def get_tags(arn_to_type: dict[str, str], batch_size: int = 100) -> dict[str, dict]:
    """Fetch tags for ARNs, routing by resource type to appropriate fetcher.

    Args:
        arn_to_type: Mapping of ARN -> resource_type
        batch_size: Batch size for standard API (max 100)

    Returns:
        Mapping of ARN -> tags dict
    """
    if not arn_to_type:
        raise ValueError("arn_to_type cannot be empty")

    # Group ARNs by fetcher
    standard_arns: list[str] = []
    custom_groups: dict[Fetcher, list[str]] = defaultdict(list)

    for arn, resource_type in arn_to_type.items():
        fetcher = RESOURCE_TAG_GETTERS.get(resource_type)
        if fetcher:
            custom_groups[fetcher].append(arn)
        else:
            standard_arns.append(arn)

    # Fetch via standard API
    tags = get_tags_standard(standard_arns, batch_size)

    # Fetch via custom fetchers
    for fetcher, arns in custom_groups.items():
        tags.update(fetcher(arns))

    return tags


def set_tags(changes: list[TagChange]) -> SetTagsResult:
    """Apply tag changes, routing by resource type to appropriate setter.

    Args:
        changes: List of TagChange objects

    Returns:
        SetTagsResult with success/failed ARNs
    """
    if not changes:
        return SetTagsResult()

    # Group changes by setter
    standard_changes: dict[str, dict[str, str]] = {}
    custom_groups: dict[Setter, dict[str, dict[str, str]]] = defaultdict(dict)

    for change in changes:
        setter = RESOURCE_TAG_SETTERS.get(change.resource_type)
        if setter:
            custom_groups[setter][change.arn] = change.tags_to_set
        else:
            standard_changes[change.arn] = change.tags_to_set

    result = SetTagsResult()

    # Apply via standard API
    if standard_changes:
        standard_results = set_tags_standard(standard_changes)
        for arn, success in standard_results.items():
            if success:
                result.success.append(arn)
            else:
                result.failed[arn] = "Failed to set tags"

    # Apply via custom setters
    for setter, arn_to_tags in custom_groups.items():
        setter_results = setter(arn_to_tags)
        for arn, success in setter_results.items():
            if success:
                result.success.append(arn)
            else:
                result.failed[arn] = "Failed to set tags"

    return result
