"""Wizard interactivo para guiar al usuario en la conversión."""
import typer
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pathlib import Path

from docmorph.core.config import SUPPORTED_EXTENSIONS, DEFAULT_SEARCH_PATH
from docmorph.core.console import console
from docmorph.core.external_tools import check_pandoc
from docmorph.search.engine import run_search
from docmorph.converters.manager import ConversionManager


def run_wizard() -> None:
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
        console.print("Output saved to same directory.")
    else:
        console.print("[bold red]Conversion failed.[/]")
        raise typer.Exit(code=1)
