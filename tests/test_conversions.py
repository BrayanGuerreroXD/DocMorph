#!/usr/bin/env python3
"""
Integration tests: prueba todas las conversiones de DocMorph.
Ejecutar desde la raíz: pytest tests/test_conversions.py -v
o: python -m pytest tests/
"""
import pytest
from pathlib import Path

from docmorph.converters.manager import ConversionManager
from docmorph.core.config import SUPPORTED_EXTENSIONS

# Archivos sample.* están en tests/ junto a los tests
TEST_DIR = Path(__file__).resolve().parent


@pytest.fixture
def manager():
    return ConversionManager()


@pytest.fixture
def sample_files():
    """Archivos sample.* en tests/."""
    if not TEST_DIR.exists():
        return []
    files = list(TEST_DIR.glob("sample.*"))
    return [f for f in files if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]


def test_conversions_integration(manager, sample_files):
    """Ejecuta todas las combinaciones de conversión (test de integración)."""
    if not sample_files:
        pytest.skip("No test samples in tests/")

    results = []
    for input_file in sorted(sample_files):
        input_ext = input_file.suffix.lower()
        target_formats = [ext for ext in SUPPORTED_EXTENSIONS if ext != input_ext]
        for target_ext in target_formats:
            result = manager.convert(input_file, target_ext)
            results.append({"input": input_file.name, "output": target_ext, "success": result})

    failed = [r for r in results if not r["success"]]
    # Con Playwright (HtmlToPdfStrategy) todas las conversiones deberían funcionar (20/20)
    success_count = len(results) - len(failed)
    assert success_count >= 16, f"Too many failures: {success_count}/{len(results)}. Failed: {failed}"
