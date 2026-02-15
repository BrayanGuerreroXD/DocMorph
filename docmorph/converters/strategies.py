from pathlib import Path
from abc import ABC, abstractmethod

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
        # TODO: Implement Phase 6
        return False

class MarkItDownStrategy(ConversionStrategy):
    """
    Conversion strategy using MarkItDown (Microsoft).
    """
    def convert(self, input_file: Path, output_file: Path) -> bool:
        # TODO: Implement Phase 6
        return False
