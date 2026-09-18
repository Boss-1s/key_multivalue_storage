#pylint: skip-file
from __future__ import annotations

__lazy_modules__ = ["typing.Any", "typing.Callable"]

from .utils import metadata as meta
from typing import Any, Callable

def help() -> None: ...
def print(*args, **kwargs) -> None: ...

class Delete(metaclass=meta._DeleteMeta):
    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None: ...
    @classmethod
    def by_propkey(cls, file_path: str, top_lv_key: Any, property_key: str) -> None: ...
    @classmethod
    def by_key(cls, file_path: str, key: Any) -> None: ...
    @staticmethod
    def all(file_path: str, warn: bool = True) -> None: ...
