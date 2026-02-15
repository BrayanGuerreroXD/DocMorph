from pathlib import Path
from typing import Dict, Optional
from docmorph.core.console import console
from docmorph.converters.strategies import (
    ConversionStrategy,
    PandocStrategy,
    MarkItDownStrategy,
    PipelineStrategy,
    HtmlToPdfStrategy,
)


class ConversionManager:
    """
    Manages document conversion strategies.
    Uses the Strategy Pattern to select the appropriate converter based on input/output formats.
    """
    def __init__(self):
        self._strategies: Dict[str, ConversionStrategy] = {
            "pandoc": PandocStrategy(),
            "markitdown": MarkItDownStrategy(),
        }
        self._pipeline = PipelineStrategy(
            self._strategies["markitdown"],
            self._strategies["pandoc"],
        )
        self._html_to_pdf = HtmlToPdfStrategy(
            self._strategies["pandoc"],
            self._pipeline,
        )

    def register_strategy(self, key: str, strategy: ConversionStrategy):
        self._strategies[key] = strategy

    def get_strategy(self, input_ext: str, output_ext: str) -> ConversionStrategy:
        """
        Selects the best strategy for the given conversion.
        """
        input_ext = input_ext.lower()
        output_ext = output_ext.lower()

        # PDF -> DOCX or PDF -> HTML: Pipeline (PDF->MD->target)
        if input_ext == '.pdf' and output_ext in ['.docx', '.html']:
            return self._pipeline

        # Microsoft formats or PDF to Markdown/TXT -> Use MarkItDown
        if output_ext in ['.md', '.txt'] and input_ext in ['.pdf', '.pptx', '.xlsx']:
            return self._strategies["markitdown"]

        # Output PDF: HtmlToPdfStrategy (Input->HTML->PDF) sin pdflatex ni wkhtmltopdf
        if output_ext == '.pdf':
            return self._html_to_pdf

        # Default to Pandoc for everything else
        return self._strategies["pandoc"]

    def convert(self, input_file: Path, output_format: str, output_file: Optional[Path] = None) -> bool:
        """
        Executes the conversion.
        If output_file is provided, writes there; otherwise uses input_file.with_suffix(output_format).
        """
        if not input_file.exists():
            console.print(f"[bold red]File not found: {input_file}[/]")
            return False

        # Ensure format has dot
        if not output_format.startswith('.'):
            output_format = f".{output_format}"

        if output_file is None:
            output_file = input_file.with_suffix(output_format)
        
        # Avoid overwriting input file
        if output_file == input_file:
            console.print("[yellow]Output file would be same as input. Appending '_converted'.[/]")
            output_file = input_file.with_stem(f"{input_file.stem}_converted")

        strategy = self.get_strategy(input_file.suffix.lower(), output_format.lower())
        console.print(f"[dim]Using strategy: {strategy.__class__.__name__}[/]")

        return strategy.convert(input_file, output_file)
