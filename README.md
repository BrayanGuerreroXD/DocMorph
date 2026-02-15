# 🦋 DocMorph - Document Transformation CLI

**DocMorph** is a modern and powerful Command Line Interface (CLI) tool designed to transform documents between multiple formats quickly, intuitively, and without friction.

---

## 🚀 Key Features

1.  **Interactive Wizard**: Scans your current directory and guides you step-by-step through the conversion process.
2.  **Zero-Config**: Automatically manages external dependencies (like Pandoc) without any user intervention.
3.  **Smart Search**: High-performance recursive search engine that skips system folders (e.g., `.git`, `venv`) and gracefully handles permission errors.
4.  **Extensible Architecture**: Built using the *Strategy Pattern* to always select the best conversion engine for each format.

---

## 📂 Supported Formats

| Output Format | Supported Input Formats | Engine Used |
| :--- | :--- | :--- |
| **.docx** | PDF, MD, HTML, TXT | Pandoc / Pipeline |
| **.pdf** | DOCX, MD, HTML, TXT | Pandoc (HTML via weasyprint) |
| **.md** | PDF, DOCX, PPTX, XLSX, HTML | MarkItDown / Pandoc |
| **.html** | PDF, DOCX, MD, TXT | Pandoc |
| **.txt** | PDF, DOCX, MD, HTML | MarkItDown / Pandoc |

> [!NOTE]
> Only modern Word documents (**DOCX**) are supported. Legacy `.doc` files are not compatible.

---

## 🛠️ Requirements & Installation

### Prerequisites
*   **Python 3.12** or higher installed on your system.

### Environment Setup
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

---

## 💻 Usage Modes

### 1. Interactive Mode (Wizard)
Ideal for searching files on disk and converting them visually.
```bash
python -m docmorph.main
```

### 2. Command Line Mode (Direct)
For automation or fast conversion of known files.
```bash
python -m docmorph.main convert path/to/input.pdf output.md
```

### Other Options
```bash
python -m docmorph.main --version  # Show current version
python -m docmorph.main --help     # Show full help
```

---

## 🏗️ Project Structure

```text
docmorph/
├── main.py             # Entry point and TUI logic
├── core/
│   ├── config.py       # Global configurations and constants
│   └── dependencies.py  # External tool manager (Pandoc)
├── search/
│   └── engine.py       # Performance-oriented search engine
└── converters/
    ├── manager.py      # Conversion orchestrator (Strategy Pattern)
    └── strategies.py   # Specific transformation implementations
```

---

## 🧬 Tech Stack

We selected the best Python libraries to ensure stability and a premium user experience:

*   **Typer**: For building the CLI interface with strong typing.
*   **Rich**: For a stunning visual interface with tables, colors, and animations.
*   **InquirerPy**: For modern interactive menus with **Fuzzy Search**.
*   **MarkItDown & Pandoc**: Robust conversion engines integrated transparently.

---

## 🤝 Key Design Decisions

*   **Environment Isolation**: Designed to run exclusively in virtual environments to prevent dependency conflicts.
*   **Smart Selection**: The `ConversionManager` dynamically chooses between **Pandoc** and **MarkItDown** (by Microsoft) depending on which one provides the best output quality for the specific file type.
*   **Resilience**: The search engine uses `os.scandir` for maximum speed and automatically skips protected folders without interrupting execution.

---

## 🔮 Roadmap

- [ ] Implement comprehensive unit tests with `pytest`.
- [ ] Add support for batch/bulk folder conversion.
- [ ] Persistent logging system in `core/config.py`.
- [ ] Asynchronous optimization for scanning large disk drives.
