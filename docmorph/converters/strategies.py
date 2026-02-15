import pypandoc
from pathlib import Path
from abc import ABC, abstractmethod
from rich.console import Console

console = Console()

class ConversionStrategy(ABC):
    """
    Abstract base class for all conversion strategies.
    Defines the interface that all converters must implement.
    """
    @abstractmethod
    def convert(self, input_file: Path, output_file: Path) -> bool:
        pass

class PandocStrategy(ConversionStrategy):
    """
    Conversion strategy using Pandoc via pypandoc.
    """
    def convert(self, input_file: Path, output_file: Path) -> bool:
        try:
            output_format = output_file.suffix.replace('.', '')
            # pypandoc requires string paths
            pypandoc.convert_file(str(input_file), output_format, outputfile=str(output_file))
            return True
        except RuntimeError as e:
            console.print(f"[bold red]Pandoc Error:[/] {e}")
            return False
        except Exception as e:
            console.print(f"[bold red]Unexpected Error during Pandoc conversion:[/] {e}")
            return False

class MarkItDownStrategy(ConversionStrategy):
    """
    Conversion strategy using MarkItDown (Microsoft).
    Best for converting complex formats (PDF, PPTX, XLSX) to Markdown.
    """
    def convert(self, input_file: Path, output_file: Path) -> bool:
        try:
            from markitdown import MarkItDown
            md = MarkItDown()
            result = md.convert(str(input_file))
            
            if result and result.text_content:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
                return True
            return False
        except ImportError:
             console.print("[bold red]MarkItDown library not installed/found.[/]")
             return False
        except Exception as e:
            console.print(f"[bold red]MarkItDown Error:[/] {e}")
            return False
