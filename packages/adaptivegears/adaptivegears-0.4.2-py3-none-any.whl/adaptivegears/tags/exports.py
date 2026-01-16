"""Export AWS resource tags to XLSX."""

from pathlib import Path

import boto3
import pandas as pd
from rich.console import Console

from .tags import get_tags

console = Console()

TAG_COLUMNS = ["Workload", "Component", "Name", "UUID"]

# Resource type -> (taggable, cost_relevant)
# https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_supported-resources-enforcement.html
RESOURCE_TYPES: dict[str, tuple[bool, bool]] = {
    "acm:certificate": (
        True,
        True,
    ),
    "apigateway:restapis": (
        True,
        True,
    ),
    "apigateway:restapis/deployments": (
        False,
        False,
    ),
    "apigateway:restapis/resources": (
        False,
        False,
    ),
    "apigateway:restapis/resources/methods": (
        False,
        False,
    ),
    "apigateway:restapis/stages": (
        True,
        False,
    ),
    "apprunner:autoscalingconfiguration": (
        True,
        False,
    ),
    "athena:datacatalog": (
        True,
        False,
    ),
    "athena:workgroup": (
        True,
        True,
    ),
    "autoscaling:autoScalingGroup": (
        True,
        True,
    ),  # TODO: use autoscaling:CreateOrUpdateTags
    "backup:backup-plan": (
        True,
        False,
    ),
    "backup:backup-vault": (
        True,
        True,
    ),
    "ce:anomalymonitor": (
        True,
        False,
    ),
    "ce:anomalysubscription": (
        True,
        False,
    ),
    "cloudformation:stack": (
        True,
        True,
    ),
    "cloudfront:cache-policy": (
        False,
        False,
    ),
    "cloudfront:distribution": (
        True,
        True,
    ),
    "cloudfront:function": (
        False,
        False,
    ),
    "cloudfront:origin-access-control": (
        False,
        False,
    ),
    "cloudfront:origin-access-identity": (
        False,
        False,
    ),
    "cloudtrail:trail": (
        True,
        True,
    ),
    "cloudwatch:alarm": (
        True,
        True,
    ),
    "cloudwatch:dashboard": (
        False,
        False,
    ),
    "codebuild:project": (
        True,
        True,
    ),
    "codecommit:repository": (
        True,
        True,
    ),
    "codedeploy:application": (
        True,
        False,
    ),
    "codepipeline:pipeline": (
        True,
        True,
    ),
    "datasync:location": (
        True,
        False,
    ),
    "datasync:task": (
        True,
        True,
    ),
    "dms:subgrp": (
        True,
        False,
    ),
    "dynamodb:table": (
        True,
        True,
    ),
    "ec2:dhcp-options": (
        True,
        False,
    ),
    "ec2:elastic-ip": (
        True,
        True,
    ),
    "ec2:fleet": (
        True,
        False,
    ),
    "ec2:image": (
        True,
        True,
    ),
    "ec2:instance": (
        True,
        True,
    ),
    "ec2:internet-gateway": (
        True,
        False,
    ),
    "ec2:key-pair": (
        True,
        False,
    ),
    "ec2:launch-template": (
        True,
        True,
    ),
    "ec2:natgateway": (
        True,
        True,
    ),
    "ec2:network-acl": (
        True,
        False,
    ),
    "ec2:network-interface": (
        True,
        False,
    ),
    "ec2:placement-group": (
        True,
        False,
    ),
    "ec2:reserved-instances": (
        True,
        True,
    ),
    "ec2:route-table": (
        True,
        False,
    ),
    "ec2:security-group": (
        True,
        False,
    ),
    "ec2:security-group-rule": (
        True,
        False,
    ),
    "ec2:snapshot": (
        True,
        True,
    ),
    "ec2:spot-instances-request": (
        True,
        True,
    ),
    "ec2:subnet": (
        True,
        False,
    ),
    "ec2:volume": (
        True,
        True,
    ),
    "ec2:vpc": (
        True,
        False,
    ),
    "ec2:vpc-endpoint": (
        True,
        True,
    ),
    "ec2:vpc-peering-connection": (
        True,
        False,
    ),
    "ecr:repository": (
        True,
        True,
    ),
    "eks:cluster": (
        True,
        True,
    ),
    "eks:daemonset": (
        False,
        False,
    ),
    "eks:deployment": (
        False,
        False,
    ),
    "eks:endpointslice": (
        False,
        False,
    ),
    "eks:ingress": (
        False,
        False,
    ),
    "eks:namespace": (
        False,
        False,
    ),
    "eks:persistentvolume": (
        False,
        False,
    ),
    "eks:replicaset": (
        False,
        False,
    ),
    "eks:service": (
        False,
        False,
    ),
    "eks:statefulset": (
        False,
        False,
    ),
    "elasticache:cluster": (
        True,
        True,
    ),
    "elasticache:parametergroup": (
        True,
        True,
    ),
    "elasticache:replicationgroup": (
        True,
        True,
    ),
    "elasticache:reserved-instance": (
        True,
        True,
    ),
    "elasticache:subnetgroup": (
        True,
        True,
    ),
    "elasticache:user": (
        True,
        True,
    ),
    "elasticfilesystem:file-system": (
        True,
        True,
    ),
    "elasticloadbalancing:listener-rule/app": (
        True,
        False,
    ),
    "elasticloadbalancing:listener/app": (
        True,
        False,
    ),
    "elasticloadbalancing:listener/net": (
        True,
        False,
    ),
    "elasticloadbalancing:loadbalancer": (
        True,
        True,
    ),
    "elasticloadbalancing:loadbalancer/app": (
        True,
        True,
    ),
    "elasticloadbalancing:loadbalancer/net": (
        True,
        True,
    ),
    "elasticloadbalancing:targetgroup": (
        True,
        True,
    ),
    "es:domain": (
        True,
        True,
    ),
    "events:event-bus": (
        True,
        True,
    ),
    "events:rule": (
        True,
        True,
    ),
    "glue:database": (
        True,
        False,
    ),
    "glue:table": (
        False,
        False,
    ),
    "guardduty:detector": (
        True,
        True,
    ),
    "iam:group": (
        False,
        False,
    ),
    "iam:instance-profile": (
        True,
        False,
    ),
    "iam:mfa": (
        True,
        False,
    ),
    "iam:oidc-provider": (
        True,
        False,
    ),
    "iam:policy": (
        True,
        False,
    ),
    "iam:role": (
        True,
        False,
    ),
    "iam:server-certificate": (
        True,
        False,
    ),
    "iam:user": (
        True,
        False,
    ),
    "inspector:target/template": (
        True,
        False,
    ),
    "kms:key": (
        True,
        True,
    ),
    "lambda:function": (
        True,
        True,
    ),
    "logs:log-group": (
        True,
        True,
    ),
    "memorydb:acl": (
        True,
        False,
    ),
    "memorydb:parametergroup": (
        True,
        False,
    ),
    "memorydb:user": (
        True,
        False,
    ),
    "mq:configuration": (
        True,
        False,
    ),
    "rds:auto-backup": (
        False,
        False,
    ),
    "rds:cluster": (
        True,
        True,
    ),
    "rds:cluster-pg": (
        True,
        False,
    ),
    "rds:cluster-snapshot": (
        True,
        True,
    ),
    "rds:db": (
        True,
        True,
    ),
    "rds:deployment": (
        True,
        False,
    ),
    "rds:og": (
        True,
        False,
    ),
    "rds:pg": (
        True,
        False,
    ),
    "rds:ri": (
        True,
        True,
    ),
    "rds:secgrp": (
        True,
        False,
    ),
    "rds:snapshot": (
        True,
        True,
    ),
    "rds:subgrp": (
        True,
        False,
    ),
    "resource-explorer-2:index": (
        False,
        False,
    ),
    "resource-explorer-2:view": (
        False,
        False,
    ),
    "resource-groups:group": (
        True,
        False,
    ),
    "route53:healthcheck": (
        True,
        True,
    ),
    "route53:hostedzone": (
        True,
        True,
    ),
    "route53resolver:resolver-query-log-config": (
        True,
        False,
    ),
    "s3:bucket": (
        True,
        True,
    ),
    "s3:storage-lens": (
        True,
        False,
    ),
    "secretsmanager:secret": (
        True,
        True,
    ),
    "ses:configuration-set": (
        True,
        False,
    ),
    "ses:identity": (
        True,
        False,
    ),
    "sns:topic": (
        True,
        True,
    ),
    "sqs:queue": (
        True,
        True,
    ),
    "ssm:association": (
        True,
        False,
    ),
    "ssm:document": (
        True,
        False,
    ),
    "ssm:managed-instance": (
        True,
        False,
    ),
    "ssm:parameter": (
        True,
        True,
    ),
    "ssm:resource-data-sync": (
        False,
        False,
    ),
    "wafv2:ipset": (
        True,
        False,
    ),
    "wafv2:rulegroup": (
        True,
        False,
    ),
    "wafv2:webacl": (
        True,
        True,
    ),
}


def get_resources() -> list[dict]:
    """Fetch all resources via Resource Explorer 2."""
    client = boto3.client("resource-explorer-2")
    paginator = client.get_paginator("list_resources")

    resources = []
    for page in paginator.paginate():
        resources.extend(page["Resources"])
        console.print(f"Fetched {len(resources)} resources...")
    return resources


def to_dataframe(resources: list[dict]) -> pd.DataFrame:
    """Convert API response to DataFrame with tag columns."""
    # Filter to taggable and cost-relevant resources
    filtered_resources = []
    for r in resources:
        resource_type = r["ResourceType"]
        if resource_type not in RESOURCE_TYPES:
            raise ValueError(f"Unknown resource type: {resource_type}")
        taggable, cost_relevant = RESOURCE_TYPES[resource_type]
        if taggable and cost_relevant:
            filtered_resources.append(r)

    # Build arn -> resource_type mapping for tag fetcher routing
    arn_to_type = {r["Arn"]: r["ResourceType"] for r in filtered_resources}
    tags = get_tags(arn_to_type) if arn_to_type else {}

    rows = []
    for r in filtered_resources:
        arn = r["Arn"]
        resource_type = r["ResourceType"]
        resource_tags = tags.get(arn, {})

        row = {
            "resource_type": resource_type,
            "resource_arn": arn,
        }
        for tag in TAG_COLUMNS:
            row[f"tag:{tag}"] = resource_tags.get(tag, "")
        rows.append(row)

    return pd.DataFrame(rows).sort_values("resource_arn").reset_index(drop=True)


def to_xlsx(df: pd.DataFrame, output: Path) -> None:
    """Export DataFrame to XLSX."""
    df.to_excel(output, index=False, sheet_name="Resources")
