import pypandoc
from pathlib import Path
from abc import ABC, abstractmethod
from markitdown import MarkItDown

from docmorph.core.console import console
from docmorph.converters.formats import PANDOC_INPUT_FORMAT_MAP, PANDOC_OUTPUT_FORMAT_MAP

from playwright.sync_api import sync_playwright

def _get_pandoc_input_format(ext: str) -> str:
    """Formato Pandoc para input. .txt -> markdown (plain text es markdown válido)."""
    ext_lower = ext.lower() if ext.startswith('.') else f".{ext}".lower()
    return PANDOC_INPUT_FORMAT_MAP.get(ext_lower, ext_lower.lstrip('.'))


def _get_pandoc_output_format(ext: str) -> str:
    """Formato Pandoc para output. .txt -> plain."""
    ext_lower = ext.lower() if ext.startswith('.') else f".{ext}".lower()
    return PANDOC_OUTPUT_FORMAT_MAP.get(ext_lower, ext_lower.lstrip('.'))


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
    Uses PANDOC_FORMAT_MAP for correct extension mapping (e.g. .txt -> plain).
    """
    def __init__(self, extra_args: list | None = None):
        self.extra_args = extra_args or []

    def convert(self, input_file: Path, output_file: Path) -> bool:
        try:
            input_format = _get_pandoc_input_format(input_file.suffix)
            output_format = _get_pandoc_output_format(output_file.suffix)
            # pypandoc requires string paths
            pypandoc.convert_file(
                str(input_file), output_format,
                outputfile=str(output_file),
                format=input_format,
                extra_args=self.extra_args
            )
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
            err_type = type(e).__name__
            if "Conversion" in err_type or "Unsupported" in err_type or "Format" in err_type:
                console.print(f"[bold red]MarkItDown conversion failed:[/] {e}")
            else:
                console.print(f"[bold red]MarkItDown Error:[/] {e}")
            return False


def _ensure_playwright_chromium() -> bool:
    """Asegura que Chromium esté instalado para Playwright. Descarga automática en 1ª vez."""
    import subprocess
    import sys
    try:
        with sync_playwright() as p:
            p.chromium.launch()
        return True
    except Exception:
        try:
            with console.status("[yellow]Descargando Chromium para PDF (~150MB, solo primera vez)...[/]", spinner="dots"):
                subprocess.run(
                    [sys.executable, "-m", "playwright", "install", "chromium"],
                    check=True,
                    capture_output=True,
                )
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]No se pudo instalar Chromium:[/] {e}")
            console.print("[dim]Ejecute manualmente: python -m playwright install chromium[/]")
            return False


class HtmlToPdfStrategy(ConversionStrategy):
    """
    Convierte cualquier input a PDF: Input -> HTML (Pandoc) -> PDF (Playwright/Chromium).
    No requiere pdflatex ni wkhtmltopdf. Chromium se descarga automáticamente en 1ª conversión.
    """
    def __init__(self, pandoc: PandocStrategy, pipeline: "PipelineStrategy"):
        self.pandoc = pandoc
        self.pipeline = pipeline

    def convert(self, input_file: Path, output_file: Path) -> bool:
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as tmp:
            tmp_path = Path(tmp.name)
        try:
            # Step 1: Input -> HTML
            input_ext = input_file.suffix.lower()
            if input_ext == ".pdf":
                md_tmp = tmp_path.with_suffix(".md")
                if not self.pipeline.markitdown.convert(input_file, md_tmp):
                    return False
                if not self.pandoc.convert(md_tmp, tmp_path):
                    return False
                if md_tmp.exists():
                    md_tmp.unlink()
            else:
                if not self.pandoc.convert(input_file, tmp_path):
                    return False
            # Step 2: HTML -> PDF (Playwright + Chromium, pip-only)
            if not _ensure_playwright_chromium():
                return False
            html_url = f"file://{tmp_path.resolve()}"
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(html_url, wait_until="networkidle")
                page.pdf(path=str(output_file))
                browser.close()
            return output_file.exists()
        except ImportError:
            console.print(
                "[bold red]Playwright no instalado. Ejecute: pip install playwright[/]"
            )
            return False
        except Exception as e:
            console.print(f"[bold red]Error generando PDF:[/] {e}")
            return False
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


class PipelineStrategy(ConversionStrategy):
    """
    Pipeline: PDF -> MD (MarkItDown) -> target (Pandoc).
    Pandoc cannot read PDF; MarkItDown can. Used for PDF->DOCX and PDF->HTML.
    """
    def __init__(self, markitdown: MarkItDownStrategy, pandoc: PandocStrategy):
        self.markitdown = markitdown
        self.pandoc = pandoc

    def convert(self, input_file: Path, output_file: Path) -> bool:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
            tmp_path = Path(tmp.name)
        try:
            # Step 1: PDF -> MD
            if not self.markitdown.convert(input_file, tmp_path):
                return False
            # Step 2: MD -> target
            return self.pandoc.convert(tmp_path, output_file)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
