#pylint: skip-file
from __future__ import annotations

__lazy_modules__ = ["typing.Any", "typing.Callable"]

from typing import Any, Callable

from public import public

from .utils import metadata as meta

@public
def help() -> None: ...

def print(*args, **kwargs) -> None: ...

@public
class Delete(metaclass=meta._DeleteMeta):
    @public
    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None: ...

    @public
    @classmethod
    def by_propkey(cls, file_path: str, top_lv_key: Any, property_key: str) -> None: ...

    @public
    @classmethod
    def by_key(cls, file_path: str, key: Any) -> None: ...

    @public
    @staticmethod
    def all(file_path: str, warn: bool = True) -> None: ...
