"""
Custom Warning classes and warning decorators for kms.

Best if new warnings are kept to a minimum. Always try to use existing built-in warnings.
"""
#pylint: disable=too-many-ancestors, unused-variable
from __future__ import annotations

import functools
import inspect
import sys
from collections.abc import Callable

warnings = sys.modules.get("warnings")

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
    def __init__(self, message: str | None=None, method: str | None=None) -> None:
        if not message:
            message = ("WARNING! You are strongly advised against adding a Storage "+
                      "instance and a dict/list together, as it may break the Storage "+
                      "instance that is created.")
        if not method:
            method = "unknown"

        super().__init__(message)
        self.method = method

    def __str__(self) -> str:
        return f"{self.method}: WARNING: AdditionFailureWarning: {self.args[0]}"

class SubtractionFailureWarning(RuntimeWarning):
    """
    Warns you about attempting to subtract a Storage instance by a dictionary, and vice versa.

    Also applies to division, despite the name.
    """
    def __init__(self, message: str | None=None, method: str|None=None) -> None:
        if not message:
            message = ("WARNING! You are strongly advised against subtracting/dividing a Storage "+
                      "instance and a dict/list together, as it may break the Storage "+
                      "instance that is created.")
        if not method:
            method = "unknown"

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


def _deprecated_arg[**P, R](arg_name: str,
                            message: str | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to issue a warning when a specific method argument is used."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Get the exact names of parameters the method accepts
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)

            # Check if the deprecated argument name is present in the passed arguments
            if arg_name in bound_args.arguments:
                msg = message or f"Argument '{arg_name}' in '{func.__name__}' is deprecated."
                warnings.warn(msg, DeprecationWarning, stacklevel=2) #type: ignore

            return func(*args, **kwargs)
        return wrapper
    return decorator
