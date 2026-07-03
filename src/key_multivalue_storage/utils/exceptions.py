"""
Custom Exception classes for kms

It is best if a new exception inhierited from one of the
exceptions below, or an existing exception. Otherwise,
inheirit from Exception/BaseException.
"""

from __future__ import annotations
from typing import Any

#pylint: disable=too-many-ancestors
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

class NoInstantiationError(TypeError):
    """
    Custom exception raised when attempting to instantiate a
    non-instantiable class.
    """
