"""Custom Warning classes"""

from __future__ import annotations

class DeleteWarning(UserWarning):
    """
    Warns you about deleting all contents of a database file.
    """
    def __init__(self, message: str="", method: str="") -> None:
        super().__init__(message)
        self.method = method

    def __str__(self) -> str:
        return f"{self.method}: WARNING: DeleteWarning: {self.args[0]}"

class AdditionFailureWarning(RuntimeWarning):
    """
    Warns you about attempting to add a Storage instance with a dictionary or list.
    """
    def __init__(self, message: str="", method: str="") -> None:
        super().__init__(message)
        self.method = method

    def __str__(self) -> str:
        return f"{self.method}: WARNING: AdditionFailureWarning: {self.args[0]}"

class SubtractionFailureWarning(RuntimeWarning):
    """
    Warns you about attempting to subtract a
    Storage instance by a dictionary, and vice versa.

    Also applies to division, despite the name.
    """
    def __init__(self, message: str="", method: str="") -> None:
        super().__init__(message)
        self.method = method

    def __str__(self) -> str:
        return f"{self.method}: WARNING: SubtractionFailureWarning: {self.args[0]}"

class CastWarning(SyntaxWarning):
    """
    Warns you about attempting to pass a key argument as something other than a string.
    """
    def __init__(self, message: str="", method: str="") -> None:
        super().__init__(message)
        self.method = method

    def __str__(self) -> str:
        return f"{self.method}: WARNING: CastWarning: {self.args[0]}"
