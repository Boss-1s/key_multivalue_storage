"""
Key to Multivalue Storage - 'storage' Module

This module contains the 'Storage' class. This is the
main class in which this library is centralized about.
You can create instances of this class using the format
`Storage(key, subkey=subvalue...)` and storing it in a
JSON file with `.store(file_path)`.

Made with love by Boss_1s.
(c)2025, 2026. This work is released under the GPL General License v2.0.
"""
# pylint: skip-file
from __future__ import annotations

from public import private, public

__lazy_modules__ = ["uuid"]

from collections.abc import KeysView
import uuid
from functools import total_ordering
from types import TracebackType
from typing import Any, Callable, Generator, overload
from typing_extensions import deprecated

from .utils import metadata as meta

# Top-level functions
@public
def help() -> None: ...
def print(*args: Any, **kwargs: Any) -> None: ...

@public
@total_ordering
class Storage[TopKey = str, SubKey = str, SubVal = Any](dict[Any, Any],metaclass=meta._StorageMeta):
    # Global attributes
    indent: int
    encode: bool
    auto_delete_self: bool

    # Instance attributes (Explicitly tracks your strict 3-slot types)
    instance_id: uuid.UUID
    key: TopKey
    values: dict[Any, Any] # pyright: ignore[reportIncompatibleMethodOverride]

    _default_valueerror_msg: str

    @public
    def __init__(self, key: TopKey, **kwargs: SubVal) -> None: ...
    def __init_subclass__(cls, **kwargs: Any) -> None: ...

    @private
    @staticmethod
    def _encode(string: Any) -> int: ...
    @private
    @staticmethod
    def _decode(string: str | int) -> str: ...

    @private
    def _to_dict(self, encode: bool = False) -> dict[TopKey, dict[SubKey, SubVal]]: ...

    @private
    @classmethod
    @deprecated("This private method will be removed soon.")
    def _from_dict(cls, data_dict: dict[TopKey, dict[SubKey, SubVal]], raw: bool = False) -> Storage[TopKey, SubKey, SubVal]: ...

    @public
    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None: ...

    @public
    def store(self, file_path: str, instant_delete: bool | None = None, indent: int | None = None, encode: bool | None = None) -> None: ...

    @public
    def to_dict(self) -> dict[str, dict[str, Any]]: ...
    @public
    def keys(self) -> KeysView[Any]: ... #type: ignore

    @public
    def __str__(self) -> str: ...
    @public
    def __repr__(self) -> str: ...
    @public
    def __eq__(self, other: Any) -> bool: ...
    @public
    def __lt__(self, other: Any) -> bool: ...
    @public
    def __le__(self, other: Any) -> bool: ...

    @public
    def __add__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal] | list[Any]) -> Storage[TopKey, SubKey, SubVal]: ...
    @public
    def __radd__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal]: ...
    @public
    def __sub__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal]: ...
    @public
    def __rsub__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal]: ...
    @overload
    def __truediv__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal]: ...
    @overload
    def __truediv__(self, other: int) -> list[Storage[TopKey, SubKey, SubVal]]:...
    @public
    def __truediv__(self,
                    other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal] | int
                    ) -> Storage[TopKey, SubKey, SubVal] | list[Storage[TopKey, SubKey, SubVal]]: ...
    @public
    def __rtruediv__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal]: ...

    #FIXME: needs overloads
    @public
    def __and__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal] | int: ...
    @public
    def __or__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal] | int: ... # pyright: ignore[reportIncompatibleMethodOverride]
    @public
    def __xor__(self, other: Storage[TopKey, SubKey, SubVal] | dict[SubKey, SubVal]) -> Storage[TopKey, SubKey, SubVal] | int: ...
    @public
    def __lshift__(self, other: int) -> Storage[TopKey, SubKey, SubVal] | int: ...
    @public
    def __rshift__(self, other: int) -> Storage[TopKey, SubKey, SubVal] | int: ...

    @overload
    def __getitem__(self, key: TopKey) -> dict[SubKey, SubVal]: ...
    @overload
    def __getitem__(self, key: SubKey) -> SubVal: ...
    @overload
    def __getitem__(self, key: int) -> SubVal: ...
    @overload
    def __getitem__(self, key: slice) -> list[SubVal]: ...
    @public
    def __getitem__(self,
                    key: TopKey | SubKey | int | slice) -> dict[SubKey, SubVal] | SubVal | list[SubVal]: ...

    @overload
    def __setitem__(self, key: SubKey, value: SubVal) -> None: ...
    @overload
    def __setitem__(self, key: int, value: SubVal) -> None: ...
    @public
    def __setitem__(self, key: SubKey | int, value: SubVal) -> None: ...
    @public
    def __delitem__(self, key: SubKey | int | slice) -> None: ...
    @public
    def __len__(self) -> int: ...
    @public
    def __contains__(self, item: Any) -> bool: ...

    @public
    def __iter__(self) -> Generator[TopKey | dict[SubKey, SubVal], None, None]: ...

    @public
    def __getattr__(self, name: Any) -> Any: ...
    @public
    def __setattr__(self, name: str, value: Any) -> None: ...
    @public
    def __call__(self, **kwargs: SubVal) -> None: ...
    @public
    def __enter__(self) -> dict[SubKey, SubVal]: ...
    @public
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> bool: ...
    @public
    def __format__(self, format_spec: str) -> str: ...
