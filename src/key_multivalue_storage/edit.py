"""
Key to Multivalue Storage - 'edit' Module

This module contains the 'Edit' class, a special
class created to easily edit data in JSON files.

Made with love by Boss_1s.
(c)2025, 2026. This work is released under the GPL General License v2.0.
"""
#pylint: disable=import-outside-toplevel
from __future__ import annotations

import sys
import json
import warnings
import builtins
# TODO in v1.4: import logger
from typing import Any, Callable, TYPE_CHECKING
from rich.console import Console
from rich.markdown import Markdown

from .utils import warnings as w, exceptions, metadata as meta

if TYPE_CHECKING:
    from . import Storage

def help() -> None:
    Console().print(Markdown(str(__doc__)))

def print(*args, **kwargs) -> None:
    """
    Prints the values to a stream, or to sys.stdout by default.

    sep
     string inserted between values, default a space.

    end
     string appended after the last value, default a newline.

    file
     a file-like object (stream); defaults to the current sys.stdout.

    flush
     whether to forcibly flush the stream.
    """
    builtins.print("[key_multivalue_storage/edit.py] ", *args, **kwargs)

class Edit(metaclass=meta._EditMeta):
    # TODO in v1.4: methods that allow easily `Storage` object manipulation
    # TODO in v2.0: methods should use 'subkey', 'subsubkey', etc. over 'propkey'
    """
    Class containing methods related to editing data within a JSON file.

    ### Usage
    - `Edit.propkey(file_path, top_lv_key, oldpropkey, newpropkey, new=True, noexist_ok=True) ->
    None`

    Edits the name of a subkey within a key within a JSON file. The value(s) of that subkey does
    not change.

    - `Edit.propval(file_path, top_lv_key, propkey, newval) -> None`

    Edits the value of a subkey within a key within a JSON file. The subkey of that value does
    not change.

    - `Edit.key(file_path, oldkey, newkey) -> None`

    Renames the top level key in a JSON file. The value(s) of that key does not change.


    ### Attributes
    **This class does not contain any attributes.**
    """

    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None:
        """Help function for class Load."""
        if method and not callable(method):
            raise TypeError(f"Expected callable, got '{type(method)}' instead")
        console = Console()
        help_txt: str = ''
        if method:
            console.print(Markdown(str(method.__doc__)))
        else:
            help_txt = "## **<kms.Storage.Edit>**\n" + str(cls.__doc__)
            console.print(Markdown(help_txt))
            if hasattr(sys, 'ps1'):
                console.print(Markdown("> To learn more about a specific method, "+
                                       "run `Storage.help(Storage.Edit.<method>)`. When passing "+
                                       "the method, don't call it (adding parenthesis after the "+
                                       "method name)."))

    @classmethod
    @w._deprecated_arg("new",
                      "The 'new' argument is no longer used. Please use 'noexist_ok' instead."
    )
    # TODO in v2.0: rename to subkey()
    def propkey(cls,
                file_path: str,
                top_lv_key: Any,
                oldpropkey: str,
                newpropkey: str,
                new: bool=True, # DEPRECATED
                noexist_ok: bool=True) -> None:
        """
        Edits the name of a subkey within a key within a JSON file.
        The value(s) of that subkey does not change.

        ## Arguments
        - `file_path: str`: The JSON file to load from.
        - `top_lv_key: Any`: The top level key to edit the subkey of.
        - `oldpropkey: str`: The subkey to rename.
        - `newpropkey: str`: The new name for the subkey.
        - `new: bool=True`: Deprecated. Use `noexist_ok` instead.
        - `noexist_ok: bool=True`: If True, will create a new subkey with an empty value if the old
        subkey does not exist. If False, will raise a `KeyNotFoundError` if the old subkey does
        not exist.

        ## Returns
        - `None`
        """

        from . import Storage

        if new:
            noexist_ok = new

        if not isinstance(top_lv_key, str):
            warnings.warn("It is recommended that the 'top_lv_key' value be passed as a "+
                          "string.",
                          w.CastWarning)
            top_lv_key=str(top_lv_key)

        loaded_data: Storage | None = Storage.Load.by_key(
            file_path,
            top_lv_key,
        )

        if not loaded_data:
            return

        if oldpropkey in loaded_data:
            propval = loaded_data[oldpropkey]
            del loaded_data[oldpropkey]
            loaded_data[newpropkey] = propval
        elif noexist_ok:
            warnings.warn(f"Subkey {oldpropkey} was not found. "+
                            "Creating a new subkey under the name"+
                            f" {newpropkey} with value '' (override this with"+
                            " noexist_ok=False, will raise exception)"
                            )
            loaded_data.values.update({
                newpropkey: ''
            })
        else:
            print("Edit.propkey: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path, oldpropkey)

        loaded_data.store(file_path)
        del loaded_data
        print("Edit.propkey: INFO: Sucessfully ",
                f"renamed {oldpropkey} to {newpropkey}.")

    @classmethod
    def propval(cls,
                file_path: str,
                top_lv_key: Any,
                propkey: str,
                newval: str
        ) -> None:
        # TODO in v2.0: Allow editing if propval contains Stoage objs (via MultiStorage)
        """
        Edits the value of a subkey within a key within a JSON file.
        The subkey of that value does not change.

        ## Arguments
        - `file_path: str`: The JSON file to load from.
        - `top_lv_key: Any`: The top level key to edit the subkey of.
        - `propkey: str`: The subkey to edit the value of.
        - `newval: str`: The new value for the subkey.

        ## Returns
        - `None`
        """

        from . import Storage

        print(f"Edit.propval: DEBUG: file_path={file_path}")
        print(f"Edit.propval: DEBUG: top_lv_key={top_lv_key}")
        print(f"Edit.propval: DEBUG: propkey={propkey}")
        print(f"Edit.propval: DEBUG: newval={newval}")

        if not isinstance(top_lv_key, str):
            warnings.warn("It is recommended that the 'top_lv_key' "+
                            "value be passed as a string.",
                            w.CastWarning)

        top_lv_key=str(top_lv_key)

        loaded_data: Storage | None = Storage.Load.by_key(
            file_path,
            top_lv_key,
            )

        print(f"Edit.propval: DEBUG: loaded_data={loaded_data}")
        print(f"Edit.propval: DEBUG: not loaded_data? {not loaded_data}")

        if not loaded_data:
            return

        oldval: str = ""
        for realpropkey, propval in loaded_data.values.items():
            print(f"Edit.propval: DEUBG: Current Check: {propkey} vs {realpropkey}")
            if propkey == realpropkey:
                print(f"Edit.propval: INFO: Found match for {propkey} - {realpropkey}")
                oldval = propval
                print(f"Edit.propval: DEBUG: Attempting to set {propkey} to {newval}")
                loaded_data[propkey] = newval
                break


        Storage(top_lv_key, **loaded_data.values).store(file_path)
        print(f"Edit.propval: INFO: Sucessfully changed value {oldval} "+
                f"to {newval} under key {top_lv_key}.{propkey}.")

    @classmethod
    def key(cls,
            file_path: str,
            oldkey: Any,
            newkey: Any) -> None:
        """
        Renames the top level key in a JSON file. The value(s) of that key does not change.

        ## Arguments
        - `file_path: str`: The JSON file to load from.
        - `oldkey: Any`: The top level key to rename.
        - `newkey: Any`: The new name for the top level key.

        ## Returns
        - `None`
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Edit.key: ERROR: Failed to load file '{file_path}': does not exist.")
            return
        except json.JSONDecodeError:
            print(f"Edit.key: ERROR: Failed to load file '{file_path}': contains invalid JSON.")
            return

        print(f"Edit.key: DEBUG: loaded_data.keys()={loaded_data.keys()}")
        print(f"Edit.key: DEBUG: loaded_data.values()={loaded_data.values()}")
        print(f"Edit.key: DEBUG: loaded_data={loaded_data}")

        if not isinstance(oldkey, str):
            warnings.warn("It is recommended that the 'oldkey' value be passed as a string.",
                            w.CastWarning)

        if not isinstance(newkey, str):
            warnings.warn("It is recommended that the 'newkey' value be passed as a string.",
                            w.CastWarning)

        oldkey=str(oldkey)
        newkey=str(newkey)

        if oldkey in loaded_data:
            loaded_data = {
                newkey if key == oldkey else key: value
                for key, value in loaded_data.items()
            }
            print(f"Edit.key: DEBUG: New dictionary: loaded_data={loaded_data}")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(loaded_data, f)
                    print(f"Successfully changed key '{oldkey}' to '{newkey}'.")
            except IOError as e:
                print(f"Error writing to file '{file_path}' after deletion: {e}")
        else:
            print("Edit.key: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path, oldkey)
