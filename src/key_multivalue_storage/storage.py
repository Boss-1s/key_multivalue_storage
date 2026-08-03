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
from collections.abc import Callable

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
    auto_delete_self: bool = False

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

    def store(self,
              file_path: str,
              instant_delete: bool | None = None,
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

        if instant_delete:
            del self

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
                self.values.update(other.values)
                return Storage(self.key, **self.values)
            raise ValueError(self._default_valueerror_msg)
        if isinstance(other, dict):
            warnings.warn(w.AdditionFailureWarning(method="__add__"))
            self.values.update(other)
            return Storage(self.key, **self.values)
        if isinstance(other, list):
            warnings.warn(w.AdditionFailureWarning(method="__add__"))
            self.values.update({"undefined": other})
            return Storage(self.key, **self.values)
        return NotImplemented

    def __radd__(self,
                 other: Storage | dict[str, Any]) -> Storage:
        """Defines how to add two objects, same type or no."""
        return self.__add__(other)

    def __sub__(self,
                other: Storage | dict[str, Any]
               ) -> Storage:
        """Defines how to subtract two objects, same type or no."""
        if isinstance(other, type(self)):
            if self.key==other.key:
                skeys: set = set(self.values.keys()) & set(other.values.keys())
                for akey in skeys:
                    akey: str
                    if akey in self.values:
                        del self.values[akey]
                    else:
                        self.values[akey] = other.values[akey]
                return Storage(self.key, **self.values)
            raise ValueError(self._default_valueerror_msg)
        if isinstance(other, dict):
            warnings.warn(w.SubtractionFailureWarning(method="__sub__"))
            skeys: set = set(self.values.keys()) & set(other)
            for akey in skeys:
                akey: str
                if akey in self.values:
                    del self.values[akey]
                else:
                    self.values[akey] = dict(other.values())[akey]
            return Storage(self.key, **self.values)
        return NotImplemented

    def __rsub__(self,
                 other: Storage | dict[str, Any]
                ) -> Storage:
        """
        Defines how to subtract two objects, same type or no.
        """

        skeys: set[Any] = set()
        if isinstance(other, type(self)):
            if self.key==other.key:
                skeys = set(self.values.keys()) & set(other.values.keys())
                for akey in skeys:
                    akey: str
                    if akey in self.values:
                        del self.values[akey]
                    else:
                        self.values[akey] = other.values[akey]
                return Storage(self.key, **self.values)
            raise ValueError(self._default_valueerror_msg)
        if isinstance(other, dict):
            warnings.warn(w.SubtractionFailureWarning(method="__rsub__"))
            skeys = set(self.values.keys()) & set(other)
            for akey in skeys:
                akey: str
                if akey in self.values:
                    del self.values[akey]
                else:
                    self.values[akey] = other[akey]
            return Storage(self.key, **self.values)
        return NotImplemented

    def __truediv__(self,
                    other: Storage | dict[str, Any] | int
                   ) -> list[Storage] | Storage:
        """
        Defines how to divide two objects, same type or no.

        Note that attempting to divide a Storage instance by another instance
        or a dictionary (and vice versa) will result in the subtraction of the two.
        """
        if isinstance(other, (type(self),dict)):
            return self - other
        if isinstance(other, int):
            split: float | int = len(self.values.keys())/other
            if other > 9:
                raise ValueError("Dividing by a number greater than nine is unsupported")

            if len(self.values.keys()) == split:
                return [Storage(self.key, **self.values)]

            if split.is_integer():
                i: int = 0
                templist: list[dict[str, Any]] = []
                while i < split * other:
                    nd: dict[Any, str] = {}
                    nkey: str = list(self.values.keys())[i]
                    nd[nkey] = self.values[nkey]
                    i += 1
                    while i % split != 0:
                        nkey = list(self.values.keys())[i]
                        nd[str(nkey)] = self.values[nkey]
                        i += 1
                    templist.append(nd)
                i = 0
                returnlist: list[Storage] = []
                while i < other:
                    returnlist.append(Storage(self.key, **templist[i]))
                    i+=1
                if len(returnlist) == 1:
                    return returnlist[0]
                return returnlist
            raise ValueError(f"Cannot divide by number {other} for a "+
                             f"list length of {len(self.values.keys())}")
        return NotImplemented

    def __rtruediv__(self,
                     other: Storage | dict[str, Any]
                    ) -> Storage:
        """
        Defines how to divide two objects, same type or no.
        Note that attempting to divide a Storage instance by another instance
        or a dictionary (and vice versa) will result in the subtraction of the two.
        """
        if isinstance(other, (type(self),dict)):
            return other - self
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
        """Defines using OR (|) for bitwise operations with Storage instances and dictionaries."""
        if isinstance(other, type(self)):
            if self.key==other.key:
                skeys: set = set(self.values.keys()) | set(other.values.keys())
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
            skeys: set = set(self.values.keys()) | set(other)
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
