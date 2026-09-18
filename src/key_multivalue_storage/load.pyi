"""
Key to Multivalue Storage - 'load' Module

This module contains the 'Load' class, a special
class created for the sole purpose of loading JSON data
into Storage objects, among other things.

Made with love by Boss_1s.
(c)2025, 2026. This work is released under the GPL General License v2.0.
"""
#pylint: skip-file
from __future__ import annotations

__lazy_modules__ = [".Storage", "typing.Any", "typing.Callable"]

from . import Storage
from .utils import metadata as meta
from typing import Any, Callable

def help() -> None: ...
def print(*args, **kwargs) -> None: ...

class Load(metaclass=meta._LoadMeta):
    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None: ...
    @classmethod
    def by_key(cls, file_path: str, key: Any, raw: bool = False) -> Storage | None: ...
    @classmethod
    def by_index(cls, file_path: str, index: int, raw: bool = False) -> Storage | None: ...
    @classmethod
    def keys(cls, file_path: str) -> list[str] | None: ...
    @classmethod
    def values(cls, file_path: str, key: Any, keys: bool = False, raw: bool = True) -> list[str] | None: ...
