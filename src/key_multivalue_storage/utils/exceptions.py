from __future__ import annotations
from typing import Any

class KeyNotFoundError(KeyError):
    """Custom exception raised when a key is not found."""
    def __init__(self, file: str, mkey: Any, message="") -> None:
        self.mkey = mkey
        self.file = file
        if message == "":
            self.message = f"The following key was not found in {file}: {mkey}"
        else:
            self.message = message
        super().__init__(self.message)