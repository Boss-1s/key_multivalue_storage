# pylint: disable=unused-variable
"""
Metaclasses for kms modules.

Hiearchy:
- `type` - All metaclasses must be a child of this class, per
[PEP 3115](https://peps.python.org/pep-3115/).
- `_KmsMeta` - This is the main, overarching meta-metaclass. All subsequent metaclasses must have
this class as its metaclass.
- `_<Module>Meta` - the metaclasses specifically designed for a module, while following the
requirements set by `_KmsMeta`.

A new metaclass should be defined as:
```py
class _NameMeta(type, metaclass=_KmsMeta):
    @property
    def semver(cls): ...

    @property
    def calver(cls): ...

    @property
    def last_update(cls): ...
```
"""

from __future__ import annotations
import sys
from typing_extensions import deprecated
from rich.console import Console
from rich.text import Text

class _KmsMeta(type):
    """
    Overarching metaclass for all metaclasses in kms.
    """
    def __new__(cls, name, bases, dct):
        # Ensure the attribute exists and is a property descriptor
        for required_property in ['semver', 'calver', 'version', 'last_update']:
            if required_property not in dct or not isinstance(dct[required_property], property):
                raise TypeError(f"Class {name} must define a @property named '{required_property}'")

        return super().__new__(cls, name, bases, dct)

class _StorageMeta(type, metaclass=_KmsMeta):
    """
    Metaclass for Storage module
    """
    @property
    def semver(cls) -> str:
        """Current semnatic version of this module."""
        return "v1.3.0"

    @property
    def calver(cls) -> str:
        """Current calendar version of this module."""
        return "2026.07.25"

    @property
    def version(cls) -> str:
        """Current full version of this module."""
        return "kms-"+cls.semver+"/"+cls.calver

    @property
    def last_update(cls) -> str:
        """Date this module was last updated."""
        return "2026/07/25"

    @property
    def Load(cls):
        from key_multivalue_storage import load
        return load.Load

    @property
    def Edit(cls):
        from key_multivalue_storage import edit
        return edit.Edit

    @property
    def Delete(cls):
        from key_multivalue_storage import delete
        return delete.Delete

    @property
    @deprecated("Warnings no longer belong to the `Storage` namespace. "+
                "Consider using `kms.<WarningName>` instead. This will be removed in 2.0.")
    def CastWarning(cls):
        from key_multivalue_storage import kms_warnings
        return kms_warnings.CastWarning

    @property
    @deprecated("Warnings no longer belong to the `Storage` namespace. "+
                "Consider using `kms.<WarningName>` instead. This will be removed in 2.0.")
    def SubtractionFailureWarning(cls):
        from key_multivalue_storage import kms_warnings
        return kms_warnings.SubtractionFailureWarning

    @property
    @deprecated("Warnings no longer belong to the `Storage` namespace. "+
                    "Consider using `kms.<WarningName>` instead. This will be removed in 2.0.")
    def AdditionFailureWarning(cls):
        from key_multivalue_storage import kms_warnings
        return kms_warnings.AdditionFailureWarning

    @property
    @deprecated("Warnings no longer belong to the `Storage` namespace. "+
                    "Consider using `kms.<WarningName>` instead. This will be removed in 2.0.")
    def DeleteWarning(cls):
        from key_multivalue_storage import kms_warnings
        return kms_warnings.DeleteWarning

    def __repr__(cls) -> str:
        """
        String/Dev representation of `kms.storage.Storage`
        *class* (not instances)
        """
        console = Console()
        string: str = "class kms.storage.Storage(<uninstantiated>)"
        if hasattr(sys, 'ps1'):
            console.print("[red][bold]Woah there![/][blue] Try instantiating with [bold]`Storage("+
                          "top_lv_key, **kwargs)`[/]![/]\n")
            console.print("[italic]Need help? Run `Storage.help()` "+
                          "for more information about this class.[/italic]\n")

        else:
            console.print(Text.from_markup("[blue]Hint: try instantiating with "+
                          "[bold]`Storage(top_lv_key, **kwargs)`[/]\n\n"))

        return string

    @property
    @deprecated("The metadata var name 'VERSION' has been changed "+
                "to 'semver' since kms-semver1.3. Consider using that instead."+
                "This will be removed in 2.0.")
    def VERSION(cls) -> str:
        return cls.semver

    @property
    @deprecated("The metadata var name 'DATE_VERSION' has been changed "+
                "to 'calver' since kms-semver1.3. Consider using that instead."+
                "This will be removed in 2.0.")
    def DATE_VERSION(cls) -> str:
        return cls.calver

    @property
    @deprecated("The metadata var name 'LAST_UPDATE' has been changed "+
                "to 'last_update' since kms-semver1.3. Consider using that instead."+
                "This will be removed in 2.0.")
    def LAST_UPDATE(cls) -> str:
        return cls.last_update

class _LoadMeta(type, metaclass=_KmsMeta):
    @property
    def semver(cls) -> str:
        """Current semnatic version of this module."""
        return "v1.0.0"

    @property
    def calver(cls) -> str:
        """Current calendar version of this module."""
        return "2026.07.25"

    @property
    def version(cls) -> str:
        """Current full version of this module."""
        return "kms-"+cls.semver+"/"+cls.calver

    @property
    def last_update(cls) -> str:
        """Date this module was last updated."""
        return "2026/07/25"

    def __repr__(cls) -> str:
        """
        String/Dev representation of `kms.load.Load` *class*
        """
        console = Console()
        string: str = "class kms.load.Load(<None>)"
        if hasattr(sys, 'ps1'):
            console.print("[italic]Need help? Run `Storage.Load.help()` "+
                          "for more information about this class.[/italic]\n")

        else:
            console.print(Text.from_markup("[blue]Hint: run "+
                          "[bold]`Storage.Load.help()`\n\n"))

        return string

class _EditMeta(type, metaclass=_KmsMeta):
    @property
    def semver(cls) -> str:
        """Current semnatic version of this module."""
        return "v1.0.0"

    @property
    def calver(cls) -> str:
        """Current calendar version of this module."""
        return "2026.07.25"

    @property
    def version(cls) -> str:
        """Current full version of this module."""
        return "kms-"+cls.semver+"/"+cls.calver

    @property
    def last_update(cls) -> str:
        """Date this module was last updated."""
        return "2026/07/25"

    def __repr__(cls) -> str:
        """
        String/Dev representation of `kms.edit.Edit` *class*
        """
        console = Console()
        string: str = "class kms.edit.Edit(<None>)"
        if hasattr(sys, 'ps1'):
            console.print("[italic]Need help? Run `Storage.Edit.help()` "+
                          "for more information about this class.[/italic]\n")

        else:
            console.print(Text.from_markup("[blue]Hint: run "+
                          "[bold]`Storage.Edit.help()`\n\n"))

        return string

class _DeleteMeta(type, metaclass=_KmsMeta):
    @property
    def semver(cls) -> str:
        """Current semnatic version of this module."""
        return "v1.0.0"

    @property
    def calver(cls) -> str:
        """Current calendar version of this module."""
        return "2026.07.25"

    @property
    def version(cls) -> str:
        """Current full version of this module."""
        return "kms-"+cls.semver+"/"+cls.calver

    @property
    def last_update(cls) -> str:
        """Date this module was last updated."""
        return "2026/07/25"

    def __repr__(cls) -> str:
        """
        String/Dev representation of `kms.delete.Delete` *class*
        """
        console = Console()
        string: str = "class kms.delete.Delete(<None>)"
        if hasattr(sys, 'ps1'):
            console.print("[italic]Need help? Run `Storage.Delete.help()` "+
                          "for more information about this class.[/italic]\n")

        else:
            console.print(Text.from_markup("[blue]Hint: run "+
                          "[bold]`Storage.Delete.help()`\n\n"))

        return string
