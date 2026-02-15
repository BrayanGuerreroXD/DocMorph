"""Gestión de herramientas externas: Pandoc, motores PDF, etc."""
import shutil
import pypandoc

from docmorph.core.console import console

PDF_ENGINES = ["pdflatex", "wkhtmltopdf", "weasyprint", "context"]


def get_available_pdf_engine() -> str | None:
    """
    Returns the first available PDF engine for Pandoc.
    Pandoc uses pdflatex by default; if missing, tries alternatives.
    """
    for engine in PDF_ENGINES:
        if shutil.which(engine):
            return engine
    return None


def check_pandoc() -> bool:
    """
    Checks if Pandoc is available.
    If not, attempts to download and configure it automatically.
    """
    try:
        version = pypandoc.get_pandoc_version()
        return True
    except OSError:
        console.print("[yellow]Pandoc not found. Attempting to download...[/]")
        try:
            with console.status("[bold green]Downloading Pandoc binary... This may take a moment.[/]", spinner="dots"):
                pypandoc.download_pandoc()
            console.print("[bold green]Pandoc downloaded and installed successfully![/]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error downloading Pandoc: {e}[/]")
            console.print("[yellow]Please install Pandoc manually: https://pandoc.org/installing.html[/]")
            return False
    except Exception as e:
        console.print(f"[bold red]Unexpected error checking Pandoc: {e}[/]")
        return False
