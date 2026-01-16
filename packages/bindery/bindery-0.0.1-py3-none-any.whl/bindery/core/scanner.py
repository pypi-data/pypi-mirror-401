from pathlib import Path
from typing import List
from .models import ClassNode

class Scanner:
    def __init__(self, include_paths: List[str] = None):
        self.include_paths = include_paths or []

    def scan(self, file_path: str) -> List[ClassNode]:
        """
        Scans a C++ header file and returns a list of ClassNodes.
        (Stub implementation)
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Placeholder logic
        print(f"Scanning {file_path}...")
        return []
