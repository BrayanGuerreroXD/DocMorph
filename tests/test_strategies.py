"""Unit tests para las estrategias de conversión."""
import tempfile
from pathlib import Path

import pytest

from docmorph.converters.strategies import (
    PandocStrategy,
    MarkItDownStrategy,
    PipelineStrategy,
    ConversionStrategy,
)


class TestPandocStrategy:
    def test_convert_md_to_html(self, tmp_path):
        """MD -> HTML debería funcionar."""
        input_md = tmp_path / "input.md"
        input_md.write_text("# Hello\n\nWorld.", encoding="utf-8")
        output_html = tmp_path / "output.html"
        strategy = PandocStrategy()
        result = strategy.convert(input_md, output_html)
        assert result is True
        assert output_html.exists()
        assert "Hello" in output_html.read_text(encoding="utf-8") or "hello" in output_html.read_text(encoding="utf-8").lower()

    def test_convert_txt_to_md(self, tmp_path):
        """TXT -> MD (mapeado como markdown input -> markdown output)."""
        input_txt = tmp_path / "input.txt"
        input_txt.write_text("Plain text content", encoding="utf-8")
        output_md = tmp_path / "output.md"
        strategy = PandocStrategy()
        result = strategy.convert(input_txt, output_md)
        assert result is True
        assert output_md.exists()


class TestMarkItDownStrategy:
    def test_implements_conversion_strategy(self):
        """MarkItDownStrategy debe implementar ConversionStrategy."""
        assert issubclass(MarkItDownStrategy, ConversionStrategy)

    def test_convert_nonexistent_fails(self, tmp_path):
        """Archivo inexistente debe fallar."""
        strategy = MarkItDownStrategy()
        result = strategy.convert(tmp_path / "nofile.pdf", tmp_path / "out.md")
        assert result is False


class TestPipelineStrategy:
    def test_requires_markitdown_and_pandoc(self):
        """PipelineStrategy se construye con markitdown y pandoc."""
        markitdown = MarkItDownStrategy()
        pandoc = PandocStrategy()
        pipeline = PipelineStrategy(markitdown, pandoc)
        assert pipeline.markitdown is markitdown
        assert pipeline.pandoc is pandoc
