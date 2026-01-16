"""CLI commands for AWS tag management."""

from pathlib import Path

import typer

from .exports import to_xlsx, get_resources, to_dataframe
from .imports import from_xlsx, compute_diff, apply_changes
from .tags import get_tags

app = typer.Typer(help="AWS tag management tools")


@app.command("export")
def export_tags(
    output: Path = typer.Option(
        Path("tags.xlsx"),
        "--output",
        "-o",
        help="Output XLSX file path",
    ),
):
    """Export AWS resource tags to XLSX spreadsheet."""
    resources = get_resources()
    df = to_dataframe(resources)
    to_xlsx(df, output)
    typer.echo(f"Exported {len(df)} resources to {output}")


@app.command("import")
def import_tags(
    input_file: Path = typer.Option(
        ...,
        "--input",
        "-i",
        help="Input XLSX file path",
    ),
    apply: bool = typer.Option(
        False,
        "--apply",
        help="Actually apply changes (default is dry-run)",
    ),
):
    """Import tags from XLSX spreadsheet to AWS resources."""
    # 1. Read XLSX
    typer.echo(f"Reading {input_file}...")
    df = from_xlsx(input_file)
    typer.echo(f"Found {len(df)} resources in file")

    if df.empty:
        typer.echo("No resources in file.")
        return

    # 2. Fetch current tags for resources in XLSX
    typer.echo("Fetching current tags...")
    arn_to_type = {
        row["resource_arn"]: row["resource_type"] for _, row in df.iterrows()
    }
    current_tags = get_tags(arn_to_type)

    # 3. Compute diff
    changes = compute_diff(df, current_tags)

    # 4. Display changes
    if not changes:
        typer.echo("No changes needed.")
        return

    typer.echo(f"\nPlanned changes ({len(changes)} resources):")
    for change in changes:
        typer.echo(f"\n  {change.arn}")
        for key, value in change.tags_to_set.items():
            current = current_tags.get(change.arn, {}).get(key, "")
            if current:
                typer.echo(f"    ~ {key}: {current} -> {value}")
            else:
                typer.echo(f"    + {key}: {value}")

    total_tags = sum(len(c.tags_to_set) for c in changes)
    typer.echo(f"\nTotal: {total_tags} tags on {len(changes)} resources")

    # 5. Apply if requested
    if apply:
        confirm = typer.confirm(
            f"\nApply {total_tags} tag changes to {len(changes)} resources?"
        )
        if not confirm:
            typer.echo("Aborted.")
            raise typer.Exit(1)

        typer.echo("Applying changes...")
        result = apply_changes(changes)
        typer.echo(f"Done: {len(result.success)} success, {len(result.failed)} failed")
        for arn, error in result.failed.items():
            typer.echo(f"  FAILED {arn}: {error}")
    else:
        typer.echo("\nDry run. Use --apply to execute changes.")
