from pathlib import Path
from typing import Generator, List

def run_search(path: Path, extensions: List[str]) -> Generator[Path, None, None]:
    """
    Recursively search for files with given extensions starting from path.
    Uses os.scandir for better performance than os.walk.
    Handles PermissionError gracefully.
    """
    # TODO: Implement Phase 4 logic
    yield from [] 
