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
# TODO in v1.4: return some things as objs
# TODO in v1.3.2: logger
# TODO in v1.6: final v1.x update, bug fixes and small tweaks,
# switch over to uuidv7 library so no fallback to uuidv4 is necessary

# NOTE: SEE ROADMAP FOR MORE INFO

from __future__ import annotations

import sys
import json
import uuid
import warnings
import difflib
import builtins
# TODO in v1.3.2: import logger
from typing import Any, Generator
from types import TracebackType
from functools import total_ordering
from collections.abc import Callable, KeysView

from typing_extensions import deprecated
from rich.console import Console
from rich.markdown import Markdown

from .utils import warnings as w, exceptions, metadata as meta

# TODO in v1.3.2: logger
#logger: logging.Logger | None = None
#
#def _set_up_logger(dir: str,
#                   fname: str,
#                   lname: str,
#                   format: str = "%(levelname)s:%(name)s:%(message)s",
#                  ) -> None:
#    # Set up logging
#    os.makedirs(dir, exist_ok=True)
#    with open(dir+fname, 'w'):pass
#    logger = logging.getLogger(lname)
#    logger.setLevel(logging.INFO)
#    logger.propagate = False
#    logger.addHandler(logging.FileHandler(dir+fname).setFormatter(logging.Formatter(format)))

#def _toggle_logger(self) -> None:
#    if logger.level == logging.CRITICAL + 100:logger.setLevel(logging.INFO)
#    else:logger.setLevel(logging.CRITICAL + 100)

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
    builtins.print("[key_multivalue_storage/storage.py] ", *args, **kwargs)

@total_ordering
class Storage(metaclass=meta._StorageMeta):
    """
    Main class for monokey-multivalue storage.

    ### Usage\n
    - `Storage(key: str, **kwargs: Any)`
    -> Create an instance of the Storage class to store.\n
    - `Storage.store(file_path: str)` -> Store this instance in a JSON file

    ### Attributes

    #### Global Attributes
    > Global attributes can be set at a global scale (i.e. `Storage.attribute = value`) and affect
    > all new instances of `Storage`.

    - `indent` -> indent size of JSON files.
    - `encode` -> whether or not to encode entries.
    - `auto_delete_self` -> whether or not an instance releases from memory automatically.

    #### Instance Attributes
    > Instance attributes cannot be set unless an instance is created and assigned to a variable.

    - `instance_id` -> the specific identifier of a `Storage` instance. On creation of a new
    instance, it is automatically assigned as a `uuid.UUID` object.
    - `key` -> the top level key of a `Storage` instance.
    - `values` -> the subkey-value pairs of a `Storage` instance.
    """

    # TODO in v1.3.2: global logger

    # Define global variables: indent, encode option, and automatic object release from memory
    indent: int = 4
    encode: bool = True
    auto_delete_self: bool = False # DEPRECATED

    def __init__(self,
                 key: Any,
                 **kwargs: Any
                ) -> None:
        """
        Defines instantiation of Storage.

        See main docstring (`Storage.help()`) about required arguments.
        """
        # TODO in v1.3.2: Setup logger
        # TODO in v1.5: file_type
        # TODO in v1.6: remove fallback by adding external library
        try:
            self.instance_id = uuid.uuid7()
        except AttributeError:
            self.instance_id = uuid.uuid4()
        # ...then attempt to set values
        if not isinstance(key, str):
            warnings.warn("It is recommended that the 'key' value is passed as a string.",
                          w.CastWarning)
        self.key = str(key)
        self.values = kwargs

    def __init_subclass__(cls, **kwargs) -> None:
        """
        Method to ensure that helper classes cannot be instantiated.

        The helper classes in question are `Load`, `Edit`, and `Delete`.
        """
        super().__init_subclass__(**kwargs)

        def raise_error():
            raise exceptions.NoInstantiationError(f"Cannot instantiate class {cls.__name__}")

        cls.__new__ = raise_error()

    @staticmethod
    def _encode(string: Any) -> int:
        """
        Encodes a value using a simple character-matching system.

        ### Arguments
        - `string: Any` - The object to be encoded.

        ### Output
        - `int` - The encoded object.
        """

        if not isinstance(string, str):
            string = str(string)

        char: str = """
        `1234657809=-\\][p';/.,lokimnjuyhbtfcvgrs edxz
        awq~+_)(*&^T$%@!#REDFGSWAQZXVCBNHYUJMKI<>LOP:{}|"?><
        """

        i = 0
        output = ''
        while i < len(string):
            currentchar = string[i]
            i2: int = 0
            i3 = ''
            while i3 != currentchar:
                i3 = char[i2]
                i2 += 1
                if i3 == currentchar:
                    break
            output = f"{output}{len(str(i2))}{str(i2)}"
            i += 1
        return int(output)

    @staticmethod
    def _decode(string: str | int) -> str:
        """
        Decodes a value encoded with `Storage._encode`.

        ### Arguments
        - `string: str | int`: The encoded object.

        ### Output
        - `str`: The decoded object.
        """

        if not isinstance(string, (str, int)):
            raise TypeError("Expected encoded string or integer for decoding.")

        to_decode = str(string)

        char: str = """
        `1234657809=-\\][p';/.,lokimnjuyhbtfcvgrs edx
        zawq~+_)(*&^T$%@!#REDFGSWAQZXVCBNHYUJMKI<>LOP:{}|"?><
        """

        i = 0
        output: str = ""
        while i < len(to_decode):
            totalchars = int(to_decode[i])
            print(f"_decode: DEBUG: totalchars {totalchars}")
            currentchar = int(to_decode[i + 1 : i + 1 + totalchars])
            print(f"_decode: DEBUG: currentchar={currentchar}")
            # Bounds Check
            if not 0 <= currentchar-1 < len(char):
                raise ValueError(
                    f"Decoding error: Index {currentchar - 1} out of range of characters."
                )
            output = f"{output}{char[currentchar-1]}"
            i += 1+totalchars
        return output

    def _to_dict(self, encode: bool = False) -> dict[str, dict[str, Any]]:
        """
        Prepares a key-multivalue pair (`Storage` object) for JSON dumping.

        ## Arguements
        `encode: bool = False`: Whether to encode the values.

        ## Output
        `dict[str, dict[str, Any]]` - The `Storage` object in a `dict` representation.
        """

        if encode:
            encoded_values: dict[str, Any] = {}
            for prop_key, prop_value in self.values.items():
                encoded_values[prop_key] = self._encode(prop_value)

            return {
                self.key: encoded_values
            }

        return {
            self.key: self.values
        }

    @classmethod
    @deprecated("This private method will be removed soon.")
    def _from_dict(cls,
                   data_dict: dict[str, dict[str, Any]],
                   raw: bool=False
                  ) -> Storage:
        """
        Extracts data from a dict into seperate key-multivalue pairs,
        decoding values in the process.
        """

        print(f"_from_dict: DEBUG: data_dict={data_dict}")
        print(f"_from_dict: DEBUG: raw={raw}")

        if not isinstance(data_dict, dict) or len(data_dict) != 1:
            raise ValueError("Expected a dictionary with a single top-level key.")

        top_lv_key: str = next(iter(data_dict.keys()))
        og_nested_values: dict[str, Any] = data_dict[top_lv_key]

        print(f"_from_dict: DEBUG: top_lv_key={top_lv_key}")
        print(f"_from_dict: DEBUG: og_nested_values={og_nested_values}")

        if not isinstance(og_nested_values, dict):
            raise ValueError("Expected nested values to be a dictionary.")

        if not raw:
            for prop_key, encoded_value in og_nested_values.items():
                if isinstance(encoded_value, int):
                    try:
                        og_nested_values[prop_key] = cls._decode(string=encoded_value)
                    except ValueError:
                        continue
                else:
                    continue

        return cls(top_lv_key, **og_nested_values)

    @classmethod
    def help(cls, method: Callable[..., Any] | None = None) -> None:
        """
        Help function for class Storage.
        """
        if method and not callable(method):
            raise TypeError(f"Expected callable, got '{type(method)}' instead")
        console = Console()
        help_txt: str = ''
        if method:
            console.print(Markdown(str(method.__doc__)))
        else:
            help_txt = "## **<kms.Storage>**\n" + str(cls.__doc__)
            console.print(Markdown(help_txt))
            if hasattr(sys, 'ps1'):
                console.print(Markdown("> To learn more about a specific method, "+
                                       "run `Storage.help(Storage.<method>)`. When passing the "+
                                       "method, don't call it (adding parenthesis after the "+
                                       "method name)."))

    @w._deprecated_arg("instant_delete",
                       "The attribute `auto_delete_self` has been deprecated as of "+
                       "kms-semver1.3.1. Please using the `with` keyword instead.\n"+
                       "with Storage('temp_storage', foo='bar') as s: pass"
                      )
    def store(self,
              file_path: str,
              instant_delete: bool | None = None, # DEPRECATED
              indent: int | None = None,
              encode: bool | None = None
             ) -> None:
        """
        Stores a key-multivalue pair into a json file.

        ## Arguments
        - `file_path: str`: The path to the JSON file. If there is no file extension provided,
        ".json" will automatically be appended.
        - `instant_delete: bool | None = None`: Whether or not to delete the object from memory
        after storing. Useful in memory-limited applications.
        - `indent: int | None = None`: An integer representing the JSON file's indent.
        - `encode: bool | None = None`: Whether or not to encode the data stored. Useful in
        applications requiring privacy.

        ## Outputs
        This method does not return anything.
        """

        if indent is None:
            indent = self.indent
        if instant_delete is None:
            instant_delete = self.auto_delete_self
        if encode is None:
            encode = self.encode

        all_data: dict[str, dict[str, Any]] = {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        except FileNotFoundError:
            warnings.warn(f"store: WARNING: File '{file_path}' not found. Creating a new one.")
        except json.JSONDecodeError:
            warnings.warn(f"store: WARNING: Warning: File '{file_path}' contains "+
                          "invalid JSON. Overwriting.", SyntaxWarning)
            all_data = {}

        if not file_path.endswith(".json"):
            warnings.warn(f"'{file_path}' does not end in '.json'. Appending '.json'...")
            file_path = str(file_path) + ".json"

        all_data.update(self._to_dict(encode))

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=indent)
            print(f"store: INFO: Data for key '{self.key}' stored successfully in '{file_path}'.")
        except IOError as e:
            print(f"store: ERROR: Error writing to file '{file_path}': {e}")

        if instant_delete: # DEPRECATED
            del self

    def to_dict(self) -> dict[str, dict[str, Any]]:
        """
        Converts a Storage instance into a dictionary.

        ## Arguments
        No arguments.

        ## Returns
        - `dict[str, dict[str, Any]]`: the original instance in dict form.

        ## Notes
        This method exists only as a backup to casting a `Storage` instance directly to a `dict`
        with `dict(Storage)`.
        """
        return {self.key: self.values}

    def keys(self) -> KeysView[Any]:
        """
        Returns the top level key.

        ## Arguments
        None.

        ## Output
        `dict_views[Any]`: A `dict_views` of the top level key.

        ## Notes
        This method is provided only so casting to a `dict()` is possible. The reccommeded usage
        of getting the top level key is still `storage_instance.key`.
        """
        return {self.key: None}.keys()

    # --- #

    _default_valueerror_msg: str = "Both instances must have the same top level key"

    def __str__(self) -> str:
        """Defines how the object should be represented in a easy-to-read, user-friendly form."""
        values_str: str = ',\n'.join([
            f"    {prop}: {repr(value)}" for prop, value in self.values.items()
        ])
        return "{\n" + f"  {self.key}: {{\n{values_str}\n  }}\n" + "}"

    def __repr__(self) -> str:
        """Defines how the object should be represented in an unambiguous, dev-friendly form."""
        values_str: str = ', '.join([
            f"{prop}={repr(value)}" for prop, value in self.values.items()
        ])
        return f"Storage(top_lv_key={self.key}, key_value_pairs=[{values_str}])"

    def __eq__(self, other: Any) -> bool:
        """Defines how the object should be compared as equal."""
        if isinstance(other, type(self)):
            if self.key==other.key and self.values.items()==other.values.items():
                return True
            return False

        if isinstance(other, dict):
            if other == dict(self):
                return True
            return False

        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        """Defines how the object should be compared as less than."""
        if isinstance(other, type(self)):
            if self.key!=other.key:
                raise ValueError(self._default_valueerror_msg)
            if len(self.values.items()) < len(other.values.items()):
                return True
            return False
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        """Defines how the object should be compared as less than or equal to."""
        if isinstance(other, type(self)):
            if len(self.values.items()) < len(other.values.items()) or self==other:
                return True
            return False
        return NotImplemented

    def __add__(self,
                other: Storage | dict[str, Any] | list[Any]) -> Storage:
        """Defines how to add two objects, same type or no."""
        if isinstance(other, type(self)):
            if self.key==other.key:
                _temp_dict: dict[str, Any] = dict(self.values)
                _temp_dict.update(other.values)
                return Storage(self.key, **_temp_dict)
            raise ValueError(self._default_valueerror_msg)
        if isinstance(other, dict):
            warnings.warn(w.AdditionFailureWarning(method="__add__"))
            _temp_dict = dict(self.values)
            _temp_dict.update(other)
            return Storage(self.key, **_temp_dict)
        if isinstance(other, list):
            warnings.warn(w.AdditionFailureWarning(method="__add__"))
            _temp_dict = dict(self.values)
            _temp_dict.update({"undefined": other})
            return Storage(self.key, **_temp_dict)
        return NotImplemented

    def __radd__(self,
                 other: Storage | dict[str, Any]) -> Storage:
        """Defines how to add two objects, same type or no."""
        return self.__add__(other)

    def __sub__(self,
                other: Storage | dict[str, Any]
               ) -> Storage:
        """
        Defines subtaction of Storage objects by Storage/dict objects.

        Use the symbol `-` for operations.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `other: Storage | dict[str, Any]`: The object on the right hand-side of the
        operand, from which self will be subtracted by.

        ## Output
        - `Storage`: A `Storage` instance containing the result of the subtraction.

        ## Logic
        How subtraction works here is first, we take the bitwise `AND` for both objects. After
        that, we cycle through the set produced by the AND operation and inject the keys in that
        set (and thier matching values) back into a temporary dict, which is then passed to the
        Storage constructor as **kwargs.

        Any values stored in `other` that are not in `self` will be lost. If you want to keep those
        values, use `XOR` instead.
        """
        if not isinstance(other, (dict, Storage)):
            return NotImplemented

        _skeys = set()
        _other_dict = {}

        if isinstance(other, Storage):
            if self.key != other.key:
                raise ValueError(self._default_valueerror_msg)
            _skeys: set[str] = set(self.values.keys()) & set(other.values.keys())
            _other_dict = other.values

        elif isinstance(other, dict):
            warnings.warn(w.SubtractionFailureWarning(method="__sub__"))
            _skeys: set[str] = set(self.values.keys()) & set(other)
            _other_dict = other

        _temp_dict = dict(self.values)

        for akey in _skeys:
            if akey in _temp_dict:
                del _temp_dict[akey]
            else:
                _temp_dict[akey] = _other_dict[akey]

        return Storage(self.key, **_temp_dict)

    def __rsub__(self,
                 other: Storage | dict[str, Any]
                ) -> Storage:
        """
        See __sub__ docstring for more information.

        When this method runs, the Storage object will be treated as if it is on the left-hand
        side of the `-` operand, as opposed to its actual position on the right-hand side.
        """
        return self.__sub__(other)

    def __truediv__(self,
                    other: Storage | dict[str, Any] | int
                   ) -> list[Storage] | Storage:
        """
        Defines **true division** of Storage objects with other Storage objects, dicts, or ints.

        Use the operand `/` for operations.

        This method contains overload. See storage.pyi for each specific overload and return value.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `other: Storage | dict[str, Any]` (overload 1): The object on the right hand-side of the
        operand, from which self will be divided by.
        - `other: int` (overload 2): The object on the right-hand side of the operand, from which
        self will be divided by.

        ## Outputs
        - `list[Storage]`: Only returned on overload 2 (`other` is `int`). A list of Storage
        instances, each an equal split of the original (`self`).
        - `Storage`: Only returned on overload 1 (`other` is `Storage | dict[str, Any]`). A
        Storage object returned after subtraction.

        ## Logic
        Storage.__truediv__ has two overloads. The first represents the following signature:

        ```
        @overload
        def __truediv__(self, other: Storage | dict[str, Any]) -> Storage: ...
        ```

        This represents what happens when you pass a Storage or a dict to the right-hand side
        of the operand symbol: the values simply get subtracted. Let's look at the other overload:

        ```
        @overload
        def __truediv__(self, other: int) -> Storage: ...
        ```

        This overload represets what happens when you pass an integer to divide by. It's really
        simple: we split the Storage object into *equal parts*. For example, if we had a Storage
        object with foo=bar, baz=qax, and rad=wav, then divide it by 3, we would get a **list**
        containing three seperate Storage objects - where each Storage object contains one
        of the subkey-value pair of the original Storage object.

        ```
        >>> from key_multivalue_storage import Storage
        >>> db1 = Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")
        >>> db2 = db1 / 2
        >>> for storage in db2:
        ...     print(repr(storage))
        ...     print(len(storage))
        ...
        Storage(top_lv_key=key, key_value_pairs=[foo='bar', baz='qax', a='b'])
        3
        Storage(top_lv_key=key, key_value_pairs=[c='d', e='f', g='h'])
        3
        ```
        """
        if not isinstance(other, (Storage, dict, int)):
            return NotImplemented

        if isinstance(other, (Storage, dict)):
            return self.__sub__(other)

        if isinstance(other, int):
            if other > 9:
                # TODO in v2.0: decimal.DivisionImpossible
                raise ValueError("Dividing by a number greater than nine is unsupported")

            split: float | int = len(self.values.keys()) / other

            if len(self.values.keys()) == split:
                return [Storage(self.key, **self.values)]

            if not split.is_integer():
                # TODO in v2.0: decimal.DivisionImpossible
                raise ValueError(f"Cannot divide by number {other} for a "+
                                f"list length of {len(self.values.keys())}")

            _temp_dict: dict[str, Any] = {}
            _my_keys = list(self.values.keys())
            split = int(split)
            returnlist: list[Storage] = []

            for x in range(other):
                for y in range(split):
                    _current_key = _my_keys[(y + (x * split))]
                    _temp_dict.update({_current_key: self.values[_current_key]})
                returnlist.append(Storage(self.key, **_temp_dict))
                _temp_dict = {}

            return returnlist

    def __rtruediv__(self,
                     other: Storage | dict[str, Any]
                    ) -> Storage:
        """
        See __sub__ docstring for more info.

        When this method runs, the Storage object will be treated as if it is on the left-hand
        side of the `/` operand, as opposed to its actual position on the right-hand side.
        """
        if isinstance(other, (Storage, dict)):
            return self.__sub__(other)

        return NotImplemented

    def __and__(self,
                other: Storage | dict[str, Any]
               ) -> Storage | int:
        """Defines using AND (&) for bitwise operations with Storage instances and dictionaries."""
        if isinstance(other, type(self)):
            if self.key==other.key:
                skeys: set = set(self.values.keys()) & set(other.values.keys())
                if not skeys:
                    return 0
                rtd: dict = {}
                for akey in skeys:
                    akey: str
                    if akey in self.values:
                        rtd[akey] = self.values[akey]
                    if akey in other.values:
                        rtd[akey] = other.values[akey]
                return Storage(self.key, **rtd)
            raise ValueError(self._default_valueerror_msg)
        if isinstance(other, dict):
            skeys: set = set(self.values.keys()) & set(other)
            if not skeys:
                return 0
            rtd: dict = {}
            for akey in skeys:
                akey: str
                if akey in self.values:
                    rtd[akey] = self.values[akey]
                if akey in other.values():
                    rtd[akey] = dict(other.values())[akey]
            return Storage(self.key, **rtd)
        return NotImplemented

    def __or__(self,
               other: Storage | dict[str, Any]
              ) -> Storage | int:
        """
        Defines using the OR (|) operator for set unions between Storage objects and other Storage
        objects or dictionaries.

        Use the symbol `|` for actual operations as opposed to `Storage.__or__`.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `other: Storage | dict[str, Any]`: The object on the right hand-side of the
        operand, from which self will be unionized with.

        ## Outputs
        - `Storage` - In most cases, a `Storage` instance with the combined data will be returned.
        - `int` - On error, the interger `0` will be returned. This is fundamentally the same as
        returning `False` or `None`.
        """
        if not isinstance(other, (Storage, dict)):
            return NotImplemented

        _set_keys: set[Any] = set()
        _values: dict[Any, Any] = {}

        if isinstance(other, type(self)):
            if self.key != other.key:
                raise ValueError(self._default_valueerror_msg)

            _set_keys = set(self.values.keys()) | set(other.values.keys())
            _values = other.values

        if isinstance(other, dict):
            _set_keys = set(self.values.keys()) | set(other)
            _values = other

        if not _set_keys:
            return 0

        _return_dict: dict = {}

        for _key in _set_keys:
            if _key in self.values:
                _return_dict[_key] = self.values[_key]
            elif _key in _values:
                _return_dict[_key] = _values[_key]

        return Storage(self.key, **_return_dict)

    def __xor__(self,
                other: Storage | dict[str, Any]
               ) -> Storage | int:
        """
        Defines using XOR (^) for bitwise operations with Storage instances and dictionaries.
        """
        skeys: set[Any] = set()

        if isinstance(other, type(self)):
            if self.key==other.key:
                skeys = set(self.values.keys()) ^ set(other.values.keys())
                if not skeys:
                    return 0
                rtd: dict = {}
                for akey in skeys:
                    akey: str
                    if akey in self.values:
                        rtd[akey] = self.values[akey]
                    if akey in other.values:
                        rtd[akey] = other.values[akey]
                return Storage(self.key, **rtd)
            raise ValueError(self._default_valueerror_msg)
        if isinstance(other, dict):
            skeys = set(self.values.keys()) ^ set(other)
            if not skeys:
                return 0
            rtd: dict = {}
            for akey in skeys:
                akey: str
                if akey in self.values:
                    rtd[akey] = self.values[akey]
                if akey in other.values():
                    rtd[akey] = other[akey]
            return Storage(self.key, **rtd)
        return NotImplemented

    def __lshift__(self,
                   other: int
                  ) -> Storage | int:
        """Defines using left shifting (<<) for bitwise operations with Storage instances."""
        if isinstance(other, int):
            if other > len(self.values.keys()):
                return 0
            try:
                skeys: list = list(self.values.keys())[other:]
                if not skeys:
                    return 0
                rtd: dict = {}
                for akey in skeys:
                    akey: str
                    if akey in self.values:
                        rtd[akey] = self.values[akey]
                return Storage(self.key, **rtd)
            except IndexError:
                return 0
        return NotImplemented

    def __rshift__(self,
                   other: int
                  ) -> Storage | int:
        """Defines using right shifting (>>) for bitwise operations with Storage instances."""
        if isinstance(other, int):
            if other > len(self.values.keys()):
                return 0
            try:
                skeys: list = list(self.values.keys())[:-other]
                if not skeys:
                    return 0
                rtd: dict = {}
                for akey in skeys:
                    akey: str
                    if akey in self.values:
                        rtd[akey] = self.values[akey]
                return Storage(self.key, **rtd)
            except IndexError:
                return 0
        return NotImplemented

    def __getitem__(self,
                    key: str | int | slice
                   ) -> Any:
        """Defines how to get an item from the object."""
        if key == self.key:
            return self.values

        if isinstance(key, str):
            return self.values[key]

        if isinstance(key,int):
            return self.values[list(self.values.keys())[key]]

        if isinstance(key,slice):
            return [self.values[k] for k in list(self.values.keys())[key]]

        return NotImplemented

    def __setitem__(self,
                    key: str | int, value: Any
                   ) -> None:
        """Defines how to set an item in the object to another value."""
        if isinstance(key, str):
            self.values[key] = value
        elif isinstance(key, int):
            self.values[list(self.values.keys())[key]] = value

    def __delitem__(self,
                    key: str | int | slice
                   ) -> None:
        """Defines how to delete an item in the object."""
        if isinstance(key, str):
            del self.values[key]
        elif isinstance(key, (int,slice)):
            del self.values[str(list(self.values.keys())[key])]

    def __len__(self) -> int:
        """Returns the length of the object."""
        return len(self.values.keys())

    def __contains__(self, item: Any) -> bool:
        """Defines how the object reacts to the 'in' keyword."""
        return item in self.values

    def __iter__(self) -> Generator[str|uuid.UUID|dict[str,Any], None, None]:
        """Defines how the object will act in an iteration loop."""
        counter = 0
        while counter <= len(self.values):
            if counter == 0:
                yield self.key
            elif counter > 0:
                yield {
                    list(self.values.keys())[counter-1]:
                    self.values[list(self.values.keys())[counter-1]]
                }
            counter+=1

    def __getattr__(self, name: Any) -> None:
        """Fallback function for handling an attempt to call an undefined attribute."""
        cm = difflib.get_close_matches(name,
                                       self.__dict__.keys(),
                                       n=1,
                                       cutoff=0.5)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'" +
                             (f". Did you mean '{cm[0]}'?" if cm else ""))

    def __setattr__(self,
                    name: str,
                    value: Any
                   ) -> None:
        """Handles attribute setting attempts."""
        print(f"__setattr__: INFO: Attempting to set '{name}' to '{value}'")
        super().__setattr__(name, value)
        if name == "auto_delete_self":
            warnings.warn("The attribute `auto_delete_self` has been deprecated as of "+
                          "kms-semver1.3.1. Please using the `with` keyword instead.\n"+
                          "with Storage('temp_storage', foo='bar') as s: pass",
                          DeprecationWarning)

    def __call__(self, **kwargs) -> None:
        """Defines what happens when an instance is called as a function."""
        print(f"__call__: INFO: updating Storage object {self.instance_id} with {kwargs}")
        self.values.update(kwargs)

    def __enter__(self) -> dict:
        """Defines the begginning interaction with the 'with' keyword"""
        print("__enter__: INFO: Acquring storage from object")
        return dict(self.values)

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: TracebackType | None
                ) -> bool:
        """Defines ending interaction with the 'with' keyword"""
        print("__exit__: INFO: Releasing storage from object")
        if exc_type:
            print(f"__exit__: ERROR: \n{exc_type}:\n{exc_tb}\n{exc_val}")
            return False
        return True

    def __format__(self, format_spec: str) -> str:
        """Defines interaction with format() and within f-strings."""
        rtn: str = repr(self)
        if format_spec == '.dictf':
            rtn = str({self.key: {**self.values}}) # full storage
        elif format_spec == '.dictt':
            rtn = str(self.values) #truncated top level key
        elif format_spec == '.tuplef':
            # DEPRECATED: remove in 2.0
            warnings.warn("The '.tuplef' format specifier has been deprecated and will be "+
                          "removed in v2.0.", DeprecationWarning)
            rtn = str(tuple({self.key: self.values}))
        elif format_spec == '.tuplet':
            # DEPRECATED: remove in 2.0
            warnings.warn("The '.tuplet' format specifier has been deprecated and will be "+
                          "removed in v2.0.", DeprecationWarning)
            rtn = str(tuple(self.values))
        elif format_spec == '.key':
            rtn = str(self.key)
        elif format_spec == '.keys':
            rtn = str(list(self.values.keys()))
        elif format_spec == '.values':
            rtn = str(list(self.values.values()))
        return rtn
