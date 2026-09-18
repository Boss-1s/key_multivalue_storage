#pylint: skip-file
from __future__ import annotations

__lazy_modules__ = ["typing.Any", "typing.Callable"]

from .utils import metadata as meta
from typing import Any, Callable

def help() -> None: ...
def print(*args, **kwargs) -> None: ...

class Edit(metaclass=meta._EditMeta):
    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None: ...
    @classmethod
    def propkey(cls, file_path: str, top_lv_key: Any, oldpropkey: str, newpropkey: str, new: bool = True, noexist_ok: bool = True) -> None: ...
    @classmethod
    def propval(cls, file_path: str, top_lv_key: Any, propkey: str, newval: str) -> None: ...
    @classmethod
    def key(cls, file_path: str, oldkey: Any, newkey: Any) -> None: ...
