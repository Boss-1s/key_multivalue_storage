"""
Custom Exception classes for kms

It is best if a new exception inhierited from one of the
exceptions below, or an existing exception. Otherwise,
inheirit from Exception/BaseException.
"""

from __future__ import annotations
import sys
from typing import Any

from public import public

#pylint: disable=too-many-ancestors
@public
class KeyNotFoundError(KeyError):
    """
    Custom exception raised when a key is not found.

    Example: if attempting to search for a nonexistent key with
    `Storage.Load.by_key`, this would be raised.
    """
    def __init__(self, file: str, mkey: Any, message="") -> None:
        self.mkey = mkey
        self.file = file
        if message == "":
            self.message = f"The following key was not found in {file}: {mkey}"
        else:
            self.message = message
        super().__init__(self.message)

@public
class NoInstantiationError(TypeError):
    """
    Custom exception raised when attempting to instantiate a
    non-instantiable class.

    Example: if attempting to instantiate a helper class like `Load`,
    this would be raised.

    **On the `kms-semver1.x` series, this functionality is currently *broken*.** To see it fixed,
    set the `kms.nextgen` attribute to `True`.
    """

@public
class BadBitwiseOperation(TypeError):
    """
    Custom exception raised on invalid or internal errors within bitwise operations.

    Example: if attempting to perform AND (&) and an empty set is resulted, this would be raised.

    Warning: This exception is exclusive to NextGen Preview; keeping `kms.nextgen` off will
    treat this exception as nonexistent.
    """
    def __init__(self, message="") -> None:
        if not getattr(sys.modules["key_multivalue_storage"], "nextgen", False):
            raise TypeError(f"module `{self.__module__}` has no attribute `{ \
                                self.__class__.__name__ \
                            }`. Did you forget to set `kms.nextgen` to `{ \
                                not getattr(sys.modules['key_multivalue_storage'],
                                            'nextgen',
                                            False) \
                            }`?")
        if message == "":
            self.message = "Invalid or internal error occurred within bitwise operation."
        else:
            self.message = message
        super().__init__(self.message)

@public
class EncodingError(ValueError):
    """
    Custom exception raised when an encoding operation fails.

    Example: if attempting to encode data with an unsupported encoding strategy, this would be raised.
    """
    def __init__(self, message="") -> None:
        if message == "":
            self.message = "An internal error occurred during the encoding operation."
        else:
            self.message = message
        super().__init__(self.message)
