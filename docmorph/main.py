import typer
from typing import Optional
from pathlib import Path

from docmorph.core.config import SUPPORTED_EXTENSIONS
from docmorph.core.console import console
from docmorph.core.external_tools import check_pandoc
from docmorph.converters.manager import ConversionManager
from docmorph.ui.wizard import run_wizard

__app_name__ = "docmorph"
__version__ = "0.1.0"

app = typer.Typer(
    name=__app_name__,
    help="DocMorph: A modern CLI for document transformation.",
    add_completion=False,
)


def _version_callback(value: bool):
    if value:
        console.print(f"[bold green]{__app_name__}[/] version [bold yellow]{__version__}[/]")
        raise typer.Exit()


@app.command("convert")
def convert_cmd(
    input_path: Path = typer.Argument(..., help="Input file path"),
    output_path: Path = typer.Argument(..., help="Output file path"),
):
    """Convert a file non-interactively: docmorph convert input.pdf output.md"""
    if not input_path.exists():
        console.print(f"[bold red]File not found: {input_path}[/]")
        raise typer.Exit(code=1)
    if not check_pandoc():
        console.print("[bold red]Critical dependency missing. Exiting.[/]")
        raise typer.Exit(code=1)
    output_ext = output_path.suffix.lower()
    if output_ext not in SUPPORTED_EXTENSIONS:
        console.print(f"[bold red]Unsupported output format: {output_ext}[/]")
        raise typer.Exit(code=1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manager = ConversionManager()
    success = manager.convert(input_path, output_ext, output_file=output_path)
    if not success:
        raise typer.Exit(code=1)
    console.print(f"[bold green]Saved to {output_path}[/]")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    """
    DocMorph: Transform documents between formats effortlessly.
    Run without arguments to start the interactive wizard.
    """
    if ctx.invoked_subcommand is None and not version:
        run_wizard()


if __name__ == "__main__":
    app()
