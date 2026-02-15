import os
from pathlib import Path

APP_NAME = "DocMorph"
APP_VERSION = "0.1.0"
DEFAULT_SEARCH_PATH = Path(os.getcwd())

# Configuration for file extensions supported by default
# Solo DOCX (Word moderno); .doc (Word 97-2003) eliminado por falta de soporte en Pandoc
SUPPORTED_EXTENSIONS = [".docx", ".md", ".pdf", ".html", ".txt"]


def get_app_info() -> str:
    return f"{APP_NAME} v{APP_VERSION}"
