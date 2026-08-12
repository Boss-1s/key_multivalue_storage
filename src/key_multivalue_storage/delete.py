"""
Key to Multivalue Storage - 'delete' Module

This module contains the 'Delete' class, a special
class created for the sole purpose of deleting data from
JSON files.

Made with love by Boss_1s.
(c)2025, 2026. This work is released under the GPL General License v2.0.
"""
#pylint: disable=import-outside-toplevel
from __future__ import annotations

import sys
import json
import warnings
import builtins
from typing import Any, Callable
# TODO in v1.3.2: import logger

from rich.console import Console
from rich.markdown import Markdown

from .utils import warnings as w, exceptions, metadata as meta

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
    builtins.print("[key_multivalue_storage/delete.py] ", *args, **kwargs)

class Delete(metaclass=meta._DeleteMeta):
    # TODO in v1.4: methods should allow easy Storage manipulation
    # TODO in v2.0: methods should use 'subkey', 'subsubkey', etc. over 'propkey'
    """
    Class contaning methods that allow deletion of data in JSON files.

    ### Usage
    - `Storage.Delete.by_propkey(file_path, top_lv_key, property_key) -> None`

    Deletes a property within a top-level key in the JSON file.

    - `Storage.Delete.by_key(file_path, key) -> None`

    Deletes a key-multivalue pair and its values within a JSON file.

    - `Storage.Delete.all(file_path, warn=True) -> None`

    Deletes all data stored in a JSON file.

    ### Attributes
    **This class does not contain any attributes.**
    """

    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None:
        """Help function for class Delete."""
        if method and not callable(method):
            raise TypeError(f"Expected callable, got '{type(method)}' instead")
        console = Console()
        help_txt: str = ''
        if method:
            console.print(Markdown(str(method.__doc__)))
        else:
            help_txt = "## **<kms.Storage.Delete>**\n" + str(cls.__doc__)
            console.print(Markdown(help_txt))
            if hasattr(sys, 'ps1'):
                console.print(Markdown("> To learn more about a specific method, "+
                                        "run `Storage.Delete.help(Storage.Delete.<method>)`. When"+
                                        " passing the method, don't call it (adding parenthesis "+
                                        "after the method name)."))

    @classmethod
    def by_propkey(cls,
                    file_path: str,
                    top_lv_key: Any,
                    property_key: str #TODO in v2.0: `subkey: str``
        ) -> None:
        """
        Deletes a property within a top-level key in the JSON file. Does NOT create a new instance
        of Storage, you will have to regrab the values to see the changes.

        ## Arguments
        - `file_path: str`: The path to the JSON file.
        - `top_lv_key: Any`: The top-level key in the JSON file.
        - `property_key: str`: The property key to delete within the top-level key.

        ## Returns
        `None`
        """

        from . import Storage

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Delete.by_propkey: ERROR: Failed to load file '{file_path}': "+
                  "does not exist.")
            return
        except json.JSONDecodeError:
            print(f"Delete.by_propkey: ERROR: Failed to load file '{file_path}': "+
                    "contains invalid JSON.")
            return

        if not isinstance(top_lv_key, str):
            warnings.warn("It is recommended that the 'top_lv_key' value be passed as a string."
                          ,w.CastWarning)
            top_lv_key=str(top_lv_key)

        if top_lv_key not in loaded_data:
            print("Delete.by_propkey: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path, top_lv_key)

        try:
            del loaded_data[top_lv_key][property_key]
        except KeyError as e:
            raise exceptions.KeyNotFoundError(file_path, e)

        try:
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(loaded_data, f)
        except IOError as e:
            print(f"Delete.by_propkey: ERROR: Error writing to file '{file_path}'",
                    f"after deletion: {e}")
        print("Delete.by_propkey: INFO: Sucessfully deleted subkey",
                f"{property_key} and its value.")

    @classmethod
    def by_key(cls,
                file_path: str,
                key: Any #TODO in v2.0: `top_lv_key: Any`
        ) -> None:
        """
        Deletes a key-multivalue pair and its values within a JSON file.
        Does NOT create a new instance of Storage, you will have to regrab the
        values to see the changes.

        ## Arguments
        - `file_path: str`: The path to the JSON file.
        - `key`: The key to delete in the JSON file.

        ## Returns
        `None`
        """
        # TODO v1.5: return_as_obj / return_from_obj
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Delete.by_key: ERROR: Failed to load file '{file_path}': does not exist.")
            return
        except json.JSONDecodeError:
            print(f"Delete.by_key: ERROR: Failed to load file '{file_path}': contains",
                    "invalid JSON.")
            return

        if not isinstance(key, str):
            warnings.warn("It is recommended that the 'key' value be passed as a string.",
                            w.CastWarning)
            key = str(key)

        print(f"Delete.by_key: DEBUG: loaded_data.keys()={loaded_data.keys()}")
        print(f"Delete.by_key: DEBUG: loaded_data.values()={loaded_data.values()}")
        print(f"Delete.by_key: DEBUG: loaded_data={loaded_data}")

        if key not in loaded_data:
            print("Delete.by_key: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path, key)

        del loaded_data[key]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(loaded_data, f)
                print(f"Delete.by_key: INFO: Successfully deleted key '{key}' from",
                        f"'{file_path}'.")
        except IOError as e:
            print(f"Delete.by_key: ERROR: Error writing to file '{file_path}'",
                    f"after deletion: {e}")


    @staticmethod
    def all(file_path: str,
            warn: bool=True) -> None:
        """
        Deletes all data stored in a JSON file.

        ## Arguments
        - `file_path: str`: File path to JSON file.
        - `warn: bool=True`: Whether to warn the user before deleting all data.
        If set to False, no warning will be shown. Ignoring kms.DeleteWarning will automatically
        set warn to False.

        ## Returns
        `None`
        """
        _warn = True
        for action, _, cat, _, _ in warnings.filters:
            if action == 'ignore' and cat=="DeleteWarning":
                _warn = False

        if not (_warn or warn):
            warnings.warn(w.DeleteWarning(
                f"You are about to delete ALL of the data inside the file {file_path}. This "+
                "is an irreversible action! If you are COMPLETELY CERTAIN about deleting all "+
                "the data, add Storage.Delete.all(file_path, warn=False) to your script. If "+
                "you never want to see this warning again, add "+
                "warnings.filterwarning(category=Storage.DeleteWarning) to your script.",
                method="Delete.all"
                )
            )
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            print(f"Delete.all: ERROR: Failed to load file '{file_path}': does not exist.")
            return
        except json.JSONDecodeError:
            print(f"Delete.all: ERROR: Failed to load file '{file_path}': contains",
                  "invalid JSON.")
            return

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
            print(f"Delete.all: INFO: Deleted all data from {file_path} sucessfully.")
