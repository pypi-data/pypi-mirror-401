"""CLI commands for AWS tag management."""

from pathlib import Path

import typer

from .exports import to_xlsx, get_resources, to_dataframe

app = typer.Typer(help="AWS tag management tools")


@app.command("export")
def export(
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
