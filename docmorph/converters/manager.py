from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from docmorph.converters.strategies import ConversionStrategy, PandocStrategy, MarkItDownStrategy

console = Console()

class ConversionManager:
    """
    Manages document conversion strategies.
    Uses the Strategy Pattern to select the appropriate converter based on input/output formats.
    """
    def __init__(self):
        self._strategies: Dict[str, ConversionStrategy] = {
            "pandoc": PandocStrategy(),
            "markitdown": MarkItDownStrategy()
        }

    def register_strategy(self, key: str, strategy: ConversionStrategy):
        self._strategies[key] = strategy

    def get_strategy(self, input_ext: str, output_ext: str) -> ConversionStrategy:
        """
        Selects the best strategy for the given conversion.
        """
        # Microsoft formats or PDF to Markdown -> Use MarkItDown
        if output_ext in ['.md', '.txt'] and input_ext in ['.pdf', '.pptx', '.xlsx']:
            return self._strategies.get("markitdown", self._strategies["pandoc"])
        
        # Default to Pandoc for everything else
        return self._strategies["pandoc"]

    def convert(self, input_file: Path, output_format: str) -> bool:
        """
        Executes the conversion.
        """
        if not input_file.exists():
            console.print(f"[bold red]File not found: {input_file}[/]")
            return False

        # Ensure format has dot
        if not output_format.startswith('.'):
            output_format = f".{output_format}"

        output_file = input_file.with_suffix(output_format)
        
        # Avoid overwriting input file
        if output_file == input_file:
            console.print("[yellow]Output file would be same as input. Appending '_converted'.[/]")
            output_file = input_file.with_stem(f"{input_file.stem}_converted")

        strategy = self.get_strategy(input_file.suffix.lower(), output_format.lower())
        
        console.print(f"[dim]Using strategy: {strategy.__class__.__name__}[/]")
        
        return strategy.convert(input_file, output_file)
