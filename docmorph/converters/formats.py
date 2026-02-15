"""Mapeos de extensiones a formatos Pandoc."""

# INPUT y OUTPUT difieren para .txt:
# - Input:  .txt -> markdown (Pandoc no tiene "plain" como input; plain text es markdown válido)
# - Output: .txt -> plain
PANDOC_INPUT_FORMAT_MAP = {
    ".txt": "markdown",
    ".md": "markdown",
    ".html": "html",
    ".docx": "docx",
}
PANDOC_OUTPUT_FORMAT_MAP = {
    ".txt": "plain",
    ".md": "markdown",
    ".html": "html",
    ".docx": "docx",
}
