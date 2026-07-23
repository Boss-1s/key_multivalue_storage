"""
Key to Multivalue Storage - 'load' Module
Last updated: 6/11/2026

This module contains the 'Load' class, a special
class created for the sole purpose of loading JSON data
into Storage objects, among other things.

Made with love by Boss_1s.
(c)2025, 2026. This work is released under the GPL General License v2.0.
"""
from __future__ import annotations

import sys
import json
import warnings
import builtins
# TODO in v1.5: import logger
from typing import Any, TYPE_CHECKING, Callable

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
    builtins.print("[key_multivalue_storage/load.py] ", *args, **kwargs)

class Load(metaclass=meta._LoadMeta):
    """
    Class containg methods related to loading JSON data into Storage objects.
    
    ### Usage
    - `Storage.Load.by_key(file_path: str, key: Any, raw: bool=False) -> Storage | None`
    -> Load a JSON file and find the key to extract a single key-multivalue pair and its values.
    - `Storage.Load.by_index(file_path: str, index: int, raw: bool=False) -> Storage | None` ->
    Load a JSON file and find the index at which to extract a single key-multivalue pair and its
    values.
    - `Storage.Load.keys(file_path: str) -> list[str] | None` -> Load a JSON file and returns the keys
    of that file.
    - `Storage.Load.values(file_path: str, key: Any, keys: bool=False, raw: bool=True) -> 
    list[str] | None` -> Loads a JSON file and returns the values under the inputted key.
    - `Storage.Load.help(method: ((Any) -> Any) | None) -> None` -> Displays the docstring of the
    specified method, or the entire Load class if no method is specified.

    ### Attributes
    **There are no attributes in this class.**
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
            help_txt = "## **<kms.Storage.Load>**\n" + str(cls.__doc__)
            console.print(Markdown(help_txt))
            if hasattr(sys, 'ps1'):
                console.print(Markdown("> To learn more about a specific method, "+
                                       "run `Storage.Load.help(Storage.Load.<method>)`. When "+
                                       "passing the method, don't call it (adding parenthesis "+
                                       "after the method name)."))

    @classmethod
    def by_key(cls,
                file_path: str,
                key: Any,
                raw: bool=False
                ) -> Storage | None:
        """
        Load a json file and find the key to extract
        a single key-multivalue pair and its values.

        ## Arguments
        - `file_path: str`: The file path to load from.
        - `key: Any`: The key to search for in the loaded data.
        - `raw: bool=False`: Whether to return the raw data or decode it.

        ## Returns
        - `Storage`: Returns a Storage object containing the loaded data if found.
        - `None`: Returns None if the key was not found or if there was an error.
        """

        from . import Storage

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Load.by_key: ERROR: Failed to load with key '{key}' -",
                    f"file '{file_path}' does not exist.")
            return None
        except json.JSONDecodeError:
            print(f"Load.by_key: ERROR: Failed to load with key '{key}' -",
                    f"file '{file_path}' contains invalid JSON.")
            return None

        if not isinstance(key, str):
            warnings.warn("It is recommended that the 'key' value is passed as a string.",
                            w.CastWarning)
        key=str(key)

        #Debug
        print(f"Load.by_key: DEBUG: Data loaded from '{file_path}': {loaded_data}")
        print(f"Load.by_key: DEBUG: Keys in loaded_data: {loaded_data.keys()}")
        print(f"Load.by_key: DEBUG: Type of loaded_data keys: {[
            type(k) for k in loaded_data.keys()
            ]}")
        print(f"Load.by_key: DEBUG: Key being searched for: '{key}'")
        print(f"Load.by_key: DEBUG: Type of search key: {type(key)}")

        # Super-detailed comparison check
        found_in_keys = False
        for k in loaded_data.keys():
            print(f"Load.by_key: DEBUG: Comparing '{key}' (len={len(key)},"+
                    f" repr={repr(key)}) with loaded key '{k}' (len={len(k)}, repr={repr(k)})")
            if key == k:
                found_in_keys = True
                print(f"Load.by_key: DEBUG: Match found for key '{key}'!")
                break

        if key in loaded_data and found_in_keys: #Use the flag from the detailed comparison
            try:
                return Storage._from_dict({key: loaded_data[key]}, raw)
            except ValueError as e:
                print(f"Load.by_key: ERROR: Error reconstructing object for key '{key}': {e}")
                return None
        else:
            print("Load.by_key: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path, key)

    @classmethod
    def by_index(cls,
                    file_path: str,
                    index: int,
                    raw: bool=False
                ) -> Storage | None:
        """
        Load a json file and find the index at which to
        extract a single key-multivalue pair and its values.

        Do note that this method bases the start index at 0.

        ## Arguments
        - `file_path: str`: The file path to load from.
        - `index: int`: The index to search by in the loaded data.
        - `raw: bool=False`: Whether to return the raw data or decode it.

        ## Returns
        - `Storage`: If sucessful, a Storage object will be returned with the loaded data.
        - `None`: Only returned on failure to load the file or if the index is out of bounds.
        """

        from . import Storage

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Failed to load by index '{index}' - file '{file_path}' does not exist.")
            return None
        except json.JSONDecodeError:
            print(f"Failed to load by index '{index}' -",
                    f"file '{file_path}' contains invalid JSON.")
            return None

        keys = list(loaded_data.keys())

        # Check if the provided index is valid
        if not 0 <= index < len(keys):
            print(f"Load.by_index: ERROR: Index '{index}' is out of bounds for the keys in",
                    f"'{file_path}'. Available keys: {len(keys)}"
                    )
            return None

        target_key: str = keys[index]
        if target_key in loaded_data:
            try:
                return Storage._from_dict({target_key: loaded_data[target_key]}, raw)
            except ValueError as e:
                print("Error reconstructing object for key",
                        f"'{target_key}' at index '{index}': {e}")
                return None
        else:
            print("Load.by_index: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path,
                                    target_key,
                                    f"Key '{target_key}' unexpectedly not found"+
                                    f" in loaded data for index '{index}'.")

    @classmethod
    def keys(cls, file_path: str) -> list[str] | None:
        """
        Load a json file and returns the keys of that file.
        
        ## Arguments
        - `file_path: str`: The file path to load from.

        ## Returns
        `list[str]`: A list containing strings of the top level keys in the loaded JSON file.
        `None`: May return None on error or if no keys were found.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Load.keys: ERROR: Failed to load file '{file_path}': does not exist.")
            return None
        except json.JSONDecodeError:
            print("Load.keys: ERROR: Failed to load file",
                    f"'{file_path}': contains invalid JSON.")
            return None

        return list(loaded_data.keys())

    @classmethod
    def values(cls,
                file_path: str,
                key: Any,
                keys: bool=False,
                raw: bool=True
                ) -> list[str] | None:
        """
        Loads a json file and returns the values under the inputed key.

        Unlike other loading methods, this one returns the raw values by default.

        Keys can also be returned as a key-value pair if keys=True.

        ## Arguments
        - `file_path: str`: The file path to load from.
        - `key: Any`: The key to search for in the loaded data.
        - `keys: bool=False`: Whether to return the values as a list of key-value pairs or
        just the values.
        - `raw: bool=True`: Whether to return the raw data or decode it.

        ## Returns
        - `list[str]`: A list containing the values under the specified key in the loaded data.
        If `keys=True`, then the list will contain key-value pairs in the format "key: value".
        - `None`: Returns None if the key was not found or if there was an error.
        """

        from . import Storage

        print(f"Load.values: DEBUG: file_path={file_path}")
        print(f"Load.values: DEBUG: key={key}")
        print(f"Load.values: DEBUG: keys={keys}")
        print(f"Load.values: DEBUG: raw={raw}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data: dict[str, dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Load.values: ERROR: Failed to load file '{file_path}': does not exist.")
            return None
        except json.JSONDecodeError:
            print("Load.values: ERROR: Failed to load",
                    f"file '{file_path}': contains invalid JSON.")
            return None

        print(f"Load.values: DEBUG: loaded_data={loaded_data}")
        print(f"Load.values: DEBUG: key in loaded_data? {key in loaded_data}")

        if not isinstance(key, str):
            warnings.warn("It is recommended that the 'key' value is passed as a string.",
                            w.CastWarning)

        key=str(key)

        print(f"Load.values: DEBUG: dict_to_load={({key: loaded_data[key]})}")
        if key in loaded_data:
            try:
                subsection: Storage = Storage._from_dict({key: loaded_data[key]}, raw)
            except ValueError as e:
                print(f"Load.values: ERROR: Error reconstructing object for key '{key}': {e}")
                return None
        else:
            print("Load.values: ERROR: Encountered _KeyNotFoundError")
            raise exceptions.KeyNotFoundError(file_path, key)

        items: list[str] = []
        for k, val in subsection.values.items():
            if keys:
                items.append(f"{k}: {val}")
                print(f"Load.values: DEBUG: items.append(f'{k}: {val}')")
            else:
                items.append(val)
                print(f"Load.values: DEBUG: items.append({val})")
        print(f"Load.values: DEBUG: {items}")
        return items
