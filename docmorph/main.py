import typer
from rich.console import Console
from typing import Optional

__app_name__ = "docmorph"
__version__ = "0.1.0"

app = typer.Typer(
    name=__app_name__,
    help="DocMorph: A modern CLI for document transformation.",
    add_completion=False,
)
console = Console()

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pathlib import Path
from docmorph.core.config import SUPPORTED_EXTENSIONS, DEFAULT_SEARCH_PATH
from docmorph.core.dependencies import check_pandoc
from docmorph.search.engine import run_search

from docmorph.converters.manager import ConversionManager

def _version_callback(value: bool):
    if value:
        console.print(f"[bold green]{__app_name__}[/] version [bold yellow]{__version__}[/]")
        raise typer.Exit()

def run_wizard():
    """
    Interactive wizard to guide the user through the conversion process.
    """
    console.print("[bold blue]Welcome to DocMorph Wizard![/]")
    
    # 1. Check Dependencies
    if not check_pandoc():
        console.print("[bold red]Critical dependency missing. Exiting.[/]")
        raise typer.Exit(code=1)

    # 2. Search for files
    console.print(f"[green]Searching for files in {DEFAULT_SEARCH_PATH}...[/]")
    files = list(run_search(DEFAULT_SEARCH_PATH, SUPPORTED_EXTENSIONS))
    
    if not files:
        console.print("[yellow]No supported files found in the current directory.[/]")
        raise typer.Exit()

    # 3. Select File
    file_choices = [Choice(f, name=f"{f.name} ({f.parent.name})") for f in files]
    
    selected_file = inquirer.fuzzy(
        message="Select a file to convert:",
        choices=file_choices,
        multiselect=False,
    ).execute()
    
    if not selected_file:
        return

    # 4. Select Output Format
    input_ext = selected_file.suffix.lower()
    target_formats = [ext for ext in SUPPORTED_EXTENSIONS if ext != input_ext]
    
    target_format = inquirer.select(
        message="Select output format:",
        choices=target_formats,
    ).execute()
    
    if not target_format:
        return

    # 5. Conversion
    console.print(f"[bold]Converting {selected_file.name} to {target_format}...[/]")
    
    manager = ConversionManager()
    success = manager.convert(selected_file, target_format)
    
    if success:
        console.print("[bold green]Conversion successful![/]")
        console.print(f"Output saved to same directory.")
    else:
        console.print("[bold red]Conversion failed.[/]")
        raise typer.Exit(code=1)

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
    if ctx.invoked_subcommand is None:
        run_wizard()

if __name__ == "__main__":
    app()
