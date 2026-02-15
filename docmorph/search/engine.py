import os
from pathlib import Path
from typing import Generator, List, Set, Optional

def run_search(path: Path, extensions: List[str], ignore_dirs: Optional[Set[str]] = None) -> Generator[Path, None, None]:
    """
    Recursively search for files with given extensions starting from path.
    Uses os.scandir for better performance than os.walk.
    Handles PermissionError gracefully.
    
    Args:
        path: Root path to start search from.
        extensions: List of file extensions to look for (e.g. ['.docx', '.md']).
        ignore_dirs: Set of directory names to ignore. Defaults to common system dirs.
    """
    if ignore_dirs is None:
        ignore_dirs = {'.git', 'venv', '__pycache__', 'node_modules', '.idea', '.vscode'}

    try:
        with os.scandir(path) as scanner:
            for entry in scanner:
                # Skip hidden files/directories and ignored directories
                if entry.name.startswith('.'):
                    continue
                
                if entry.is_dir(follow_symlinks=False):
                    if entry.name in ignore_dirs:
                        continue
                    # Recursively yield from subdirectories
                    try:
                        yield from run_search(Path(entry.path), extensions, ignore_dirs)
                    except PermissionError:
                        continue
                
                elif entry.is_file(follow_symlinks=False):
                    if any(entry.name.lower().endswith(ext.lower()) for ext in extensions):
                        yield Path(entry.path)
                        
    except PermissionError:
        # Skip directories we don't have access to
        return
    except OSError:
        # Handle other OS errors gracefully
        return
