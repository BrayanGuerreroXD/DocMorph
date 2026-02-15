# 🦋 DocMorph - Document Transformation CLI

**DocMorph** is a modern and powerful Command Line Interface (CLI) tool designed to transform documents between multiple formats (**DOCX, MD, PDF, HTML, TXT**) quickly, intuitively, and without friction. (Only DOCX is supported for Word; legacy .doc is not.)

---

## 🎯 Project Vision

The goal is to create a "Swiss Army knife" for document conversion that is:
1.  **Intuitive**: Scans and detects what you want to do or guides you with an interactive assistant.
2.  **Robust**: Gracefully handles conversion errors and file permissions.
3.  **Zero-Config**: Manages its own external dependencies (like Pandoc) transparently.

---

## 🛠️ Technology Stack

We selected a modern Python stack for the best developer and user experience:

| Technology | Justification | Key Advantage |
| :--- | :--- | :--- |
| **Typer** | Built on standard Python type hints. | Minimal boilerplate and automatic type validation. |
| **Rich** | The modern standard for Python TUI. | Beautiful tables, spinners, and syntax highlighting. |
| **InquirerPy** | Feature-rich prompt library. | Keyboard-navigable menus and **Fuzzy Search**. |
| **Pypandoc** | Robust Pandoc wrapper. | Transparent management of Pandoc binaries. |
| **MarkItDown** | Microsoft's conversion tool (2024). | Optimized conversion for Office and PDF to Markdown. |

---

## 🚀 Installation & Usage

### 🔧 Prerequisites
Python 3.12 or higher installed on your system.

### 📥 Environment Setup
1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    ```
2.  **Activate the Environment**:
    ```bash
    source venv/bin/activate  # Linux/macOS
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 💻 Running the Tool
To start the **Interactive Wizard**:
```bash
python -m docmorph.main
```

To check the installed version:
```bash
python -m docmorph.main --version
```

---

## 📂 Project Structure

```text
docmorph/
├── main.py             # Entry Point (Typer + UI Logic)
├── core/
│   ├── config.py       # Global configuration and constants
│   └── dependencies.py  # Dependency manager (Pandoc handler)
├── search/
│   └── engine.py       # Recursive search engine (os.scandir)
└── converters/
    ├── manager.py      # Conversion orchestrator (Strategy Pattern)
    └── strategies.py   # Transformation implementations
```

---

## 🤝 Key Design Decisions
- **Environment Isolation**: Forced use of `python3.12-venv` to prevent global conflicts.
- **Smart Strategy Selection**: The `ConversionManager` dynamically chooses between **Pandoc** and **MarkItDown** based on the file type to maximize output quality.
- **Resilient Scanning**: The search engine automatically skips restricted directories or system folders without crashing.

---

## 🔮 Future Roadmap
1. Implement comprehensive unit tests with `pytest`.
2. Add support for batch/bulk folder conversion.
3. Integrate persistent logging in `core/config.py`.
