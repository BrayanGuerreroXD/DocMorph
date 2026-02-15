import pypandoc
from rich.console import Console
import sys

console = Console()

def check_pandoc() -> bool:
    """
    Checks if Pandoc is available. 
    If not, attempts to download and configure it automatically.
    """
    try:
        # Check if pandoc is already in the path or installed by pypandoc
        # get_pandoc_version() raises OSError if not found
        version = pypandoc.get_pandoc_version()
        # console.print(f"[dim]Pandoc version {version} found.[/]")
        return True
    except OSError:
        console.print("[yellow]Pandoc not found. Attempting to download...[/]")
        try:
            with console.status("[bold green]Downloading Pandoc binary... This may take a moment.[/]", spinner="dots"):
                # download_pandoc downloads pandoc into pypandoc's directory
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
