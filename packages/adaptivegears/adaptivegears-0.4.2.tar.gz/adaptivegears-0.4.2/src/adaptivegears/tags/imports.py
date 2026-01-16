"""Import AWS resource tags from XLSX."""

from pathlib import Path

import pandas as pd

from .exports import TAG_COLUMNS
from .tags import TagChange, SetTagsResult, set_tags


def from_xlsx(path: Path) -> pd.DataFrame:
    """Read XLSX into DataFrame."""
    return pd.read_excel(path)


def compute_diff(
    desired_df: pd.DataFrame,
    current_tags: dict[str, dict],
) -> list[TagChange]:
    """Compare desired tags vs current, return changes needed.

    Only returns changes where:
    - Desired value is non-empty AND
    - Desired value differs from current value
    """
    changes = []

    for _, row in desired_df.iterrows():
        arn = row["resource_arn"]
        resource_type = row["resource_type"]
        current = current_tags.get(arn, {})

        tags_to_set = {}
        for tag in TAG_COLUMNS:
            col_name = f"tag:{tag}"
            raw_value = row.get(col_name, "")

            # Handle pandas NaN values
            if pd.isna(raw_value):
                continue

            desired_value = str(raw_value).strip()
            current_value = current.get(tag, "")

            # Only set if desired is non-empty and different
            if desired_value and desired_value != current_value:
                tags_to_set[tag] = desired_value

        if tags_to_set:
            changes.append(TagChange(arn, resource_type, tags_to_set))

    return changes


def apply_changes(changes: list[TagChange]) -> SetTagsResult:
    """Apply tag changes to AWS resources."""
    return set_tags(changes)
