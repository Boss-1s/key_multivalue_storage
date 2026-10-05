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
class Edit(metaclass=meta._EditMeta):
    @public
    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None: ...

    @public
    @classmethod
    def propkey(cls, file_path: str, top_lv_key: Any, oldpropkey: str, newpropkey: str, new: bool = True, noexist_ok: bool = True) -> None: ...

    @public
    @classmethod
    def propval(cls, file_path: str, top_lv_key: Any, propkey: str, newval: str) -> None: ...
    
    @public
    @classmethod
    def key(cls, file_path: str, oldkey: Any, newkey: Any) -> None: ...
