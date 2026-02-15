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

def _version_callback(value: bool):
    if value:
        console.print(f"[bold green]{__app_name__}[/] version [bold yellow]{__version__}[/]")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main(
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
    """
    # If no command is provided, we will eventually launch the interactive wizard here.
    # For now, just a placeholder message if run directly.
    pass

if __name__ == "__main__":
    app()
