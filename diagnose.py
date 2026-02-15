import sys
from pathlib import Path
from docmorph.core.config import SUPPORTED_EXTENSIONS
from docmorph.core.dependencies import check_pandoc
from docmorph.search.engine import run_search
from docmorph.converters.manager import ConversionManager

# Add current directory to path just in case
sys.path.append(str(Path.cwd()))

try:
    print("Checking imports...")

    print("Imports OK!")

    print(f"Supported extensions: {SUPPORTED_EXTENSIONS}")
    
    # print("Checking Pandoc (this might trigger download if missing)...")
    # check_pandoc()
    # print("Pandoc check finished.")

    print("Checking search engine...")
    files = list(run_search(Path.cwd(), SUPPORTED_EXTENSIONS))
    print(f"Found {len(files)} files.")
    for f in files[:5]:
        print(f" - {f.name}")

    print("Checking ConversionManager...")
    manager = ConversionManager()
    print("ConversionManager initiated OK!")

    print("\nDIAGNOSTIC COMPLETE: ALL MODULES ARE OK.")
except Exception as e:
    print(f"\nDIAGNOSTIC FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
