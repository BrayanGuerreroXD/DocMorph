import sys
from pathlib import Path
from typing import Optional

import typer
import typer.core

# --- CLI Configuration & Workarounds ---

# Disable Typer's Rich help rendering to avoid compatibility bugs with Click 8.3+
# This doesn't affect our own use of Rich console for the project's UI.
typer.core.rich = None

from docmorph.converters.manager import ConversionManager
from docmorph.core.config import APP_NAME, APP_VERSION, SUPPORTED_EXTENSIONS
from docmorph.core.console import console
from docmorph.core.external_tools import check_pandoc
from docmorph.ui.wizard import run_wizard

app = typer.Typer(
    name=APP_NAME.lower(),
    help=f"{APP_NAME}: A modern CLI for document transformation.",
    add_completion=False,
)

# --- Helper Functions ---

def validate_conversion_paths(input_path: Path, output_ext: str) -> None:
    """Validates if paths and formats are correct before conversion."""
    if not input_path.exists():
        console.print(f"[bold red]File not found: {input_path}[/]")
        raise typer.Exit(code=1)

    if output_ext not in SUPPORTED_EXTENSIONS:
        console.print(f"[bold red]Unsupported output format: {output_ext}[/]")
        console.print(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        raise typer.Exit(code=1)

    if not check_pandoc():
        console.print("[bold red]Critical dependency missing: Pandoc is required.[/]")
        raise typer.Exit(code=1)

def handle_version_flag() -> None:
    """Manually handles version flags to ensure immediate exit and bypass wizard."""
    if "--version" in sys.argv or "-v" in sys.argv:
        console.print(f"[bold green]{APP_NAME.lower()}[/] version [bold yellow]{APP_VERSION}[/]")
        raise typer.Exit()

# --- Commands ---

@app.command("convert")
def convert_cmd(
    input_path: Path = typer.Argument(..., help="Input file path"),
    output_path: Path = typer.Argument(..., help="Output file path"),
):
    """Convert a file non-interactively: docmorph convert input.pdf output.md"""
    output_ext = output_path.suffix.lower()
    
    # Validation phase
    validate_conversion_paths(input_path, output_ext)
    
    # Execution phase
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manager = ConversionManager()
    
    success = manager.convert(input_path, output_ext, output_file=output_path)
    if not success:
        raise typer.Exit(code=1)
        
    console.print(f"[bold green]Successfully saved to: {output_path}[/]")

# --- Entry Point ---

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        is_eager=True,
    ),
):
    """
    DocMorph: Transform documents between formats effortlessly.
    Run without arguments to start the interactive wizard.
    """
    handle_version_flag()

    if ctx.invoked_subcommand is None:
        run_wizard()


if __name__ == "__main__":
    app()
