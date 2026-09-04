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
# TODO in v1.4: logger
# TODO in v1.6: final v1.x update, bug fixes and small tweaks,
# switch over to uuidv7 library so no fallback to uuidv4 is necessary

# NOTE: SEE ROADMAP FOR MORE INFO

from __future__ import annotations

__lazy_modules__ = ["sys",
                    "json",
                    "uuid",
                    "warnings",
                    "difflib",
                    "builtins",
                    "rich.console",
                    "rich.markdown",]

import sys
import json
import uuid
import warnings
import difflib
import builtins
# TODO in v1.4: import logger
from typing import Any, Generator
from types import TracebackType
from functools import total_ordering
from collections.abc import Callable, KeysView

from typing_extensions import deprecated
from rich.console import Console
from rich.markdown import Markdown

from .utils import warnings as w, exceptions, metadata as meta

# TODO in v1.4: logger
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

    # TODO in v1.4: global logger

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
        # TODO in v1.4: Setup logger
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
        """
        Defines how the object should be represented in a easy-to-read, user-friendly form.

        ## Arguments
        None.

        ## Output
        - `str`: An easy-to-read string representation of the object.

        ## Format
        ```json
        {
            self.key: {
                self.values
            }
        }
        ```
        """
        return json.dumps(dict(self), indent=4, default=repr)

    def __repr__(self) -> str:
        """
        Defines how the object should be represented in an unambiguous, dev-friendly form.

        ## Arguments
        None.

        ## Output
        - `str`: An unambiguous string representation of the object.

        ## Format
        `Storage(top_lv_key={self.key}, key_value_pairs={self.values})`
        """
        return f"Storage(top_lv_key={self.key}, key_value_pairs={self.values})"

    def __eq__(self, other: Any) -> bool:
        """
        Defines equality between Storage objects and other Storage objects/dicts.

        Use the `==` symbol in operations instead of directly calling `__eq__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the `==` symbol.
        - `other: Storage | dict[str, Any]`: The object on the right hand-side of the
        `==` symbol, from which self will be compared against.

        ## Output
        Per [PEP 285](https://peps.python.org/pep-0285/), this method returns a
        a boolean containing the result of the comparison.

        ## Logic
        When comparing two `Storage` objects, both the **top-level key** and the **values
        of the subkey-value pairs** must be the same for equality to be `True`.

        When comparing a `Storage` object to a `dict`, the `Storage` object is casted into a dict
        and compared against the other dict.
        """
        if not isinstance(other, (Storage, dict)):
            return NotImplemented

        if isinstance(other, type(self)):
            if self.key == other.key and self.values.items() == other.values.items():
                return True

        if isinstance(other, dict) and other == dict(self):
            return True

        return False

    def __lt__(self, other: Any) -> bool:
        """
        Defines less than comparison between Storage objects and other Storage objects.

        Use the `<` symbol in operations instead of directly calling `__lt__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the `<` symbol.
        - `other: Storage | dict[str, Any]`: The object on the right hand-side of the
        `<` symbol, from which self will be compared against.

        ## Output
        Per [PEP 285](https://peps.python.org/pep-0285/), this method returns a
        a boolean containing the result of the comparison.

        ## Logic
        When comparing two `Storage` objects, both the **top-level key** must be the same
        and the **number of subkey-value pairs** must be less than the other for the comparison
        to be `True`.

        If the top-level keys are different, a ValueError will be raised. This will change in
        `kms-semver2.0.0`.
        """
        if not isinstance(other, Storage):
            return NotImplemented

        if self.key != other.key:
            # NOTE: I can't change this logic, however in 2.0 we should make it so that instead
            # of raising ValueError, it returns False
            raise ValueError(self._default_valueerror_msg)

        if len(self.values.items()) < len(other.values.items()):
            return True
        return False

    def __le__(self, other: Any) -> bool:
        """
        Defines less than or equal comparison between Storage objects and other Storage objects.

        Use the `<=` symbol in operations instead of directly calling `__le__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the `<=` symbol.
        - `other: Storage | dict[str, Any]`: The object on the right hand-side of the
        `<=` symbol, from which self will be compared against.

        ## Output
        Per [PEP 285](https://peps.python.org/pep-0285/), this method returns a
        a boolean containing the result of the comparison.

        ## Logic
        When comparing two `Storage` objects, both the **top-level key** must be the same
        and the **number of subkey-value pairs** must be less than the other for the comparison
        to be `True`.

        Top-level keys are irrelevant here for some reason.
        """
        if not isinstance(other, Storage):
            return NotImplemented

        if len(self.values.items()) < len(other.values.items()) or self == other:
            return True

        return False

    def __add__(self,
                other: Storage | dict[str, Any] | list[Any]) -> Storage:
        """
        Defines addition of Storage objects by Storage/dict objects.

        Use the symbol `+` for operations.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `other: Storage | dict[str, Any] | list[Any]`: The object on the right hand-side of the
        operand, from which self will be added with.

        ## Output
        - `Storage`: A `Storage` instance containing the result of the addition.

        ## Logic
        When adding Storage objects:
        - If the keys are the same, the values are merged.
        - If the keys are different, a ValueError is raised.

        When adding Storage objects with a dict:
        - The values from the dict are added to the Storage object, using dict().update().
        - If a key already exists in the Storage object, its value is updated, per dict.update().

        When adding Storage objects with a list:
        - The list is added as a new value under the key "undefined" in the Storage object.

        Note that this method is functionally identical to set union/biwise AND.
        """

        if not isinstance(other, (Storage, dict, list)):
            return NotImplemented

        _temp_values: dict[Any, Any] = {}

        if isinstance(other, Storage):
            if self.key != other.key:
                raise ValueError(self._default_valueerror_msg)
            _temp_values = other.values

        if isinstance(other, dict):
            if any(isinstance(value, dict) for value in other.values()):
                warnings.warn("Passing a nested dictionary may break the addition process.",
                              RuntimeWarning)
            warnings.warn(w.AdditionFailureWarning(method="__add__"))
            _temp_values = other

        if isinstance(other, list):
            warnings.warn(w.AdditionFailureWarning(method="__add__"))
            _temp_values = {"undefined": other}

        _temp_dict: dict[str, Any] = dict(self.values)
        _temp_dict.update(_temp_values)
        return Storage(self.key, **_temp_dict)

    def __radd__(self,
                 other: Storage | dict[str, Any]) -> Storage:
        """
        See __add__ docstring.
        """
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
        """
        Defines using the AND (&) operator for set intersections between Storage objects and other
        Storage objects or dictionaries.

        Use the symbol `&` for actual operations as opposed to `Storage.__and__`.

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

            _set_keys = set(self.values.keys()) & set(other.values.keys())
            if not _set_keys:
                return 0
            _values = other.values

        if isinstance(other, dict):
            _set_keys = set(self.values.keys()) & set(other)
            if not _set_keys:
                return 0
            _values = other

        _return_dict: dict = {}
        for k in _set_keys:
            k: str
            if k in self.values:
                _return_dict[k] = self.values[k]
            if k in _values:
                _return_dict[k] = _values[k]

        return Storage(self.key, **_return_dict)

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
        Defines using the XOR (^) operator for symmetric differentiation between Storage objects
        and other Storage objects or dictionaries.

        Use the symbol `^` for operations instead of explicitly calling `Storage.__xor__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `other: Storage | dict[str, Any]`: The object on the right hand-side of the operand, from
        which self will be symmetrically differentiated by.

        ## Outputs
        - `Storage` - In most cases, a `Storage` instance with the final data will be returned.
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

            _set_keys = set(self.values.keys()) ^ set(other.values.keys())
            if not _set_keys:
                return 0
            _values = other.values

        if isinstance(other, dict):
            _set_keys = set(self.values.keys()) ^ set(other)
            if not _set_keys:
                return 0
            _values = other

        _return_dict: dict = {}
        for k in _set_keys:
            k: str
            if k in self.values:
                _return_dict[k] = self.values[k]
            if k in _values:
                _return_dict[k] = _values[k]

        return Storage(self.key, **_return_dict)

    def __lshift__(self,
                   other: int
                  ) -> Storage | int:
        """
        Defines using the left shifting (<<) operator for bitwise operations with Storage
        instances.

        Use `<<` in operations instead of explicitly calling `Storage.__lshift__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `other: int`: The integer on the right hand-side of the operand, from which self
        will be left-shifted by.

        ## Outputs
        - `Storage` - In most cases, a `Storage` instance with the final data will be returned.
        - `int` - On error, the interger `0` will be returned. This is fundamentally the same as
        returning `False` or `None`.

        ## Logic
        Left-shifting `Storage` objects is like left-shifting in binary. In binary, **when a number
        is left-shifted, all bits are moved to the left *x* times.** *Any bits that get shifted out
        are lost.* I like to think off them dropping off a cliff, never to be seen again...but I
        digress. **The same logic applies here,** except instead of bits, we are **left-shifting
        the subkey-value pairs of the `Storage` object by *x*.** Again, any pairs that fall off the
        edge of that cliff will be lost forever. Thankfully, your original reference will
        (hopefully) still be there in case anything goes very, very wrong...
        """
        if not isinstance(other, int):
            return NotImplemented

        if other > len(self.values.keys()):
            return 0

        try:
            _keys: list = list(self.values.keys())[other:]

            if not _keys:
                return 0

            _return_dict: dict = {}

            for k in _keys:
                if k in self.values:
                    _return_dict[k] = self.values[k]

            return Storage(self.key, **_return_dict)

        except IndexError:
            return 0


    def __rshift__(self,
                   other: int
                  ) -> Storage | int:
        """
    Defines using the right shifting (>>) operator for bitwise operations with Storage
    instances.

    Use `>>` in operations instead of explicitly calling `Storage.__rshift__()`.

    ## Arguments
    - `self`: The object on the left-hand side of the operand.
    - `other: int`: The integer on the right hand-side of the operand, from which self
    will be right-shifted by.

    ## Outputs
    - `Storage` - In most cases, a `Storage` instance with the final data will be returned.
    - `int` - On error, the interger `0` will be returned. This is fundamentally the same as
    returning `False` or `None`.

    ## Logic
    Right-shifting `Storage` objects is like right-shifting in binary. In binary, **when a number
    is right-shifted, all bits are moved to the right *x* times.** *Any bits that get shifted out
    are lost.* I like to think off them dropping off a cliff, never to be seen again...but I
    digress. **The same logic applies here,** except instead of bits, we are **right-shifting
    the subkey-value pairs of the `Storage` object by *x*.** Again, any pairs that fall off the
    edge of that cliff will be lost forever. Thankfully, your original reference will
    (hopefully) still be there in case anything goes very, very wrong...
        """
        if not isinstance(other, int):
            return NotImplemented

        if other > len(self.values.keys()):
            return 0

        try:
            _keys: list = list(self.values.keys())[:-other]

            if not _keys:
                return 0

            _return_dict: dict = {}

            for k in _keys:
                if k in self.values:
                    _return_dict[k] = self.values[k]

            return Storage(self.key, **_return_dict)

        except IndexError:
            return 0

    def __getitem__(self,
                    key: str | int | slice
                   ) -> Any:
        """
        Defines using bracket notation to access the values of the Storage object.

        Use `Storage[key]` in operations instead of explicitly calling
        `Storage.__getitem__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `key: str | int | slice`: The key, index, or slice to access the value(s) of the Storage
        object.

        ## Outputs
        - `Any`: The value(s) associated with the key, index, or slice.
        """
        if key == self.key:
            return self.values

        match key:
            case str():
                return self.values[key]
            case int():
                return self.values[list(self.values.keys())[key]]
            case slice():
                return [self.values[k] for k in list(self.values.keys())[key]]
            case _:
                return NotImplemented

    def __setitem__(self,
                    key: str | int,
                    value: Any
                   ) -> None:
        """
        Defines using bracket notation to assign new values to a Storage object's contents.

        Use `Storage[key] = value` in operations instead of explicitly calling
        `Storage.__setitem__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `key: str | int`: The key or index to assign the value to.
        - `value: Any`: The new value to assign to the key or index.

        ## Outputs
        - `None`: None, as this mutates the Storage object directly.
        """
        match key:
            case str():
                self.values[key] = value
            case int():
                self.values[list(self.values.keys())[key]] = value

    def __delitem__(self,
                    key: str | int | slice
                   ) -> None:
        """
        Defines using the `del` keyword on a Storage object to remove a key-value pair.

        Use `del Storage[key]` in operations instead of explicitly calling
        `Storage.__delitem__()`.

        ## Arguments
        - `self`: The object on the left-hand side of the operand.
        - `key: str | int | slice`: The key, index, or slice to remove from the Storage object.

        ## Outputs
        - `None`: None, as this mutates the Storage object directly.
        """
        match key:
            case str():
                del self.values[key]
            case int() | slice():
                del self.values[str(list(self.values.keys())[key])]

    def __len__(self) -> int:
        """
        Returns the number of subkey-value pairs in the Storage object.

        ## Arguments

        None.

        ## Outputs
        - `int`: The number of subkey-value pairs in the Storage object.
        """
        return len(self.values.keys())

    def __contains__(self, item: Any) -> bool:
        """
        Defines how Storage objects react to the `in` keyword.

        Use `item in Storage` in operations instead of explicitly calling
        `Storage.__contains__()`.

        ## Arguments
        - `item: Any`: The item to check for in the Storage object.

        ## Outputs
        - `bool`: True if the item is in the Storage object's values,
        False otherwise. **Note that this means the top-level key
        is technically not "in" the object. To check if a top-level
        key exists in a Storage object, cast it to a dict first. This
        will be fixed in kms-semver2.0.0.**
        """
        return item in self.values

    def __iter__(self) -> Generator[
            str | uuid.UUID | dict[str,Any],
            None,
            None
        ]:
        """
        Defines how Storage objects are iterated over.

        Use the `for` keyword for operations instead of explicily calling
        `Storage.__iter__()`, i.e.
        ```
        for item in Storage: pass
        ```

        ## Arguments
        None.
        """
        yield self.key
        for k, v in self.values.items():
            yield {k: v}

    def __getattr__(self, name: Any) -> None:
        """
        Fallback method when a attempt to access a nonexistent
        attribute is made. This method will raise an AttributeError with a
        helpful message suggesting the closest matching attribute name, if any.

        # Arguemnts
        - `name: Any`: The name of the attribute being accessed.

        # Outputs
        - `None`: None, as this method prints directly to `stderr`.
        """
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
        """
        Method that handles attribute setting.

        Use `Storage.attr = value` in operations instead of explicitly calling
        `Storage.__setattr__()`.
        """
        # print(f"__setattr__: INFO: Attempting to set '{name}' to '{value}'")
        super().__setattr__(name, value)
        if name == "auto_delete_self":
            warnings.warn("The attribute `auto_delete_self` has been deprecated as of "+
                          "kms-semver1.3.1. Please using the `with` keyword instead.\n"+
                          "with Storage('temp_storage', foo='bar') as s: pass\n"+
                          "This attribute will be officially removed in kms-semver2.0.0.",
                          DeprecationWarning)

    def __call__(self, **kwargs) -> None:
        """
        Defines the behavior of Storage objects when it is called as a function.

        Use `Storage(**kwargs)` in operations instead of explicitly calling
        `Storage.__call__()`.

        ## Arguments
        - `**kwargs`: The key-value pairs to update the Storage object's values with.

        ## Outputs
        - `None`: None, as this mutates the Storage object directly.

        **This functionality will be kept, though it may be replaced by a more
        unambiguous method in the near future.**
        """
        # print(f"__call__: INFO: updating Storage object {self.instance_id} with {kwargs}")
        self.values.update(kwargs)

    def __enter__(self) -> dict:
        """
        Defines beginning interaction with the 'with' keyword.

        Use `with Storage(...) as s:` in operations instead of explicitly calling
        `Storage.__enter__()`.

        ## Arguments
        None.

        ## Outputs
        - `dict`: A dictionary containing the Storage object's values.

        ## Notes
        - This method officially replaces the deprecated `auto_delete_self` attribute,
        which will be removed in kms-semver2.0.0.
        - The logic here is very weird. Instead of returning the Storage object itself,
        it returns a dict of the values. This functionality will be changed in
        kms-semver2.0.0 to match convention.
        """
        # print("__enter__: INFO: Acquring storage from object")
        return dict(self.values)

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: TracebackType | None
                ) -> bool:
        """
        Defines the end of interaction with the 'with' keyword.

        See __enter__ docstring for more information.
        """
        # print("__exit__: INFO: Releasing storage from object")
        if exc_type:
            print(f"__exit__: ERROR: \n{exc_type}:\n{exc_tb}\n{exc_val}")
            return False
        return True

    def __format__(self, format_spec: str) -> str:
        """
        Defines the string representation of the Storage object when used in f-strings or with
        format().

        ## Arguments
        - `format_spec`: A string specifying the format to use.
          - Available format specifiers:
            - `.dictf`: Full storage as a dict.
            - `.dictt`: Truncated top-level key as a dict.
            - `.tuplef`: Full storage as a tuple. (DEPRECATED)
            - `.tuplet`: Truncated top-level key as a tuple. (DEPRECATED)
            - `.key`: Only the top-level key.
            - `.keys`: Only the subkeys as a list.
            - `.values`: Only the values as a list.

        > All of these return strings, but you can convert them using ast.literal_eval().

        ## Outputs
        - `str`: The formatted string representation of the Storage object.
        """
        rtn: str = repr(self)
        match format_spec:
            case '.dictf':
                rtn = str({self.key: {**self.values}}) # full storage
            case '.dictt':
                rtn = str(self.values) #truncated top level key
            case '.tuplef':
                # DEPRECATED: remove in 2.0
                warnings.warn("The '.tuplef' format specifier has been deprecated and will be "+
                              "removed in v2.0.", DeprecationWarning)
                rtn = str(tuple({self.key: self.values})) # NOSONAR
            case '.tuplet':
                # DEPRECATED: remove in 2.0
                warnings.warn("The '.tuplet' format specifier has been deprecated and will be "+
                              "removed in v2.0.", DeprecationWarning)
                rtn = str(tuple(self.values)) # NOSONAR
            case '.key':
                rtn = str(self.key)
            case '.keys':
                rtn = str(list(self.values.keys()))
            case '.values':
                rtn = str(list(self.values.values()))
        return rtn
