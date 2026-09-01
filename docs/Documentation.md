
> [!Note]
> **To use this library, you must have Python installed on your device.**
>
> *Don't have Python? Install it here: https://python.org/downloads*

# Installation
You can install `kms` with `pip`:
```sh
pip install key-multivalue-storage
```
Or, install it with uv:
```sh
uv add key-multivalue-storage
```
You can also install the `dev` extra. This extra provides Pylint and Griffe on the side, allowing for easier development and testing.
```sh
pip install key-multivalue-storage[dev]
```
> [!warning]
> This extra is only available on versions later than kms-v1.2.2/2026.05.06b.

> [!TIP]
> No `pip` or `uv`? Install the wheel here:
> https://pypi.org/project/key-multivalue-storage/#files

# Basic Usage
> [!TIP]
> When importing just logic related to `Storage` (i.e. `Storage`, `Load`, `Edit`, `Delete`), the recommended import statement is:
> ```py
> from key_multivalue_storage import Storage # note the module name!
> ```
> Otherwise, the main recommended import statement stands as:
> ```py
> import key_multivalue_storage as kms # note the module name!
> ```
- Create a Storage object to prepare the data to be stored:
```py
from key_multivalue_storage import Storage # note the module name!
my_db = Storage("my_top_level_key", mysubkey="myvalue", myothersk="anotherval")
```
- To store the object, use `Storage.store()`.
```py
my_db.store("database.json")
```
- Load data from a JSON file back into a Storage object:
```py
my_db = Storage.Load.by_key("my_top_level_key")
print(my_db)
```
>Output:
>```json
>{
>    "my_top_level_key": {
>        "mysubkey": "myvalue",
>        "myothersk": "anotherval"
>    }
>}
>```
- Change global settings:
```py
Storage.indent = 4 #indent size of JSON files
Storage.encode = True # Whether to encode stored values
Storage.auto_delete_self = True
# Whether to automatically release the object
# from memory after certain operations
```

# Structure of the Library

> [!note]
> Certain items that aren't part of the public API and/or are part of repo systems like workflows are not shown here.

- `src/key_multivalue_storage/`
  - `storage.py` — main Storage class (core functionality)
	  - `Storage`
		  - `__init__`
		  - `store`
		  - `keys`
		  - `to_dict`
  - `load.py` — loading helpers (Load class)
	  - `Load`
		  - `by_key`
		  - `by_index`
		  - `keys`
		  - `values`
  - `edit.py` — editing helpers (Edit class)
	  - `Edit`
		  - `propkey`
		  - `propval`
		  - `key`
  - `delete.py` — deletion helpers (Delete class)
	  - `Delete`
		  - `by_key`
		  - `by_propkey`
		  - `all`
  - `utils/`
    - `exceptions.py`       — custom exceptions
	    - `KeyNotFoundError`
	    - `NoInstantiationWarning`
    - `warnings.py`         — custom warning classes and private warning decorators
	    - `DeleteWarning`
	    - `CastWarning`
	    - `AddtionFailureWarning`
	    - `SubtractionFailureWarning`
    - `metadata.py`
- `test/`
  - `test-storage.py` — **Mainstream test targeting `kms.storage`**
  - `test-load.py` — **Mainstream test targeting `kms.load`**
  - `test-edit.py` — **Mainstream test targeting `kms.edit`**
  - `test-delete.py` — **Mainstream test targeting `kms.delete`**
  - `test-general.py` — *legacy, only used to ensure backwards compatibility*
  - `test-meta.py` — **Mainstream test targeting `kms.utils.metadata`**
  - `test-exceptions.py` — **Mainstream test targeting `kms.utils.exceptions` and `kms.utils.warnings`**
  - `test-fix-*.py` / `test-feat-*.py` — Targeted tests from PRs. **Integrated into mainstream tests every minor update**, starting from `kms-semver1.4.x`.

# Main Classes

> [!note]
> Note that each main class **has a help() method**, accessible via `<class>.help()`. These `help()` methods are simply docstring printers and hinters, so they will not be touched on in this documentation.

## `Storage`
The `Storage` class is the main class in this library, in which all operations revolve around. It is (so far) the only class in the library that can be instantiated.

### Arguments
- `key: Any` - Represents the **top level key** of the Storage object. Recommended to be a string, however, it is type `Any` to allow for a broader range of choices.
- `**kwargs: Any` - The keyword arguments that are converted into the instance variable `values`. It is, in technicality, a `dict[str, Any]`.

> [!important]
> These two parameters make the Storage object's type to be `dict[str, dict[str, Any]]`. 

### Attributes

#### Global Attributes

> [!note]
> Global attributes can be set at a global scale (i.e. `Storage.attribute = value`) and affect
> all new instances of `Storage`.

- `indent` -> indent size of JSON files.
- `encode` -> whether or not to encode entries.
- `auto_delete_self` -> whether or not an instance releases from memory automatically.

#### Instance Attributes

> [!note]
> Instance attributes cannot be set unless an instance is created and assigned to a variable.

- `instance_id` -> the specific identifier of a `Storage` instance. On creation of a new instance, it is automatically assigned as a `uuid.UUID` object.
- `key` -> the top level key of a `Storage` instance. Set directly by the parameter `key`.
- `values` -> the subkey-value pairs of a `Storage` instance. Set directly by the parameter `kwargs`.

### Example Usage

```py
from key_multivalue_storage import Storage

# Prepare data to be stored by wrapping it in a Storage object
simple_db = Storage("top_lv_key", subkey="value", foo="bar")

# You can also unpack a dictionary for kwargs.
my_dict: dict = {"foo": "bar", "subkey": "subval"}
from_dict = Storage("from_dict", **my_dict)

# There are also global attributes that we can change.
# Changing them will affect future instances.
Storage.indent = 4
Storage.encode = True
Storage.auto_delete_self = False

# To grab an instance's attributes, just call it.
print(simple_db.key) # Output: "top_lv_key"
print(from_dict.values) # Output: "{'foo': 'bar', 'subkey': 'subval'}"
```

### Methods

#### `Storage.store()`

```py
def store(self,
          file_path: str,
          instant_delete: bool | None = None,
          indent: int | None = None,
          encode: bool | None = None
         ) -> None:
```

Stores a key-multivalue pair (a `Storage` instance) into a JSON file.

This method must be run on a `Storage` instance for it to work properly.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|The path to the JSON file. If there is no file extension provided, ".json" will automatically be appended.|
|`instant_delete`|`bool` or `None`|`None`|Whether or not to delete the object from memory after storing. Useful in memory-limited applications. The default fallback for this if set to `None` is the instance attribute `self.auto_delete_self`.|
|`indent`|`int` or `None`|`None`|An integer representing the JSON file's indent. The default fallback for this if set to `None` is the instance attribute `self.indent`.|
|`encode`|`bool` or `None`|`None`|Whether or not to encode the data stored. Useful in applications requiring privacy. The default fallback for this if set to `None` is the instance attribute `self.encode`.|

##### Output

This method does not return anything.

##### Examples

```py
db = Storage("settings", theme="dark", timeout=30)
db.store("config.json")            # writes config.json
db.store("config", encode=True)    # will append .json -> config.json and encode values
```

### Type Hinting

Support for type hinting dropped in kms-v1.3.1/2026.08.12, along with fixing #26, meaning `Storage` can now be assigned to `dict[str, dict[str, Any]]`, along with anything type hinted as the following:
```py
Storage[TopKey, SubKey, SubVal]
```
Depending on what you type-hint on the first assignment, your type checkers will flag you down any time
- the top-level key type does not match `TopKey`
- the subkey type does not match `SubKey`
- the value type does not match `SubVal`

The default type hint, if you just pass `db: Storage = Storage(...)`, is `Storage[str, str, Any]`, which is functionally the same as `dict[str, dict[str, Any]]`.

Remember that **type-hints do not affect the actual execution of your code.** 

> [!warning]
> If you are running Python version 3.13 or earlier, you must add `from __future__ import annotations` at the top of your file to avoid a `TypeError: 'Storage' type not subscriptable` exception. This is because on 3.13 and earlier, deferred type hints had not been fully implemented yet. See [PEP 0649](https://peps.python.org/pep-0649/).

#### Examples

```py
from __future__ import annotations # Required for CPython <= 3.13

from key_multivalue_storage import Storage
from typing import Any, get_type_hints

db: Storage[str, Any, Any] = Storage("string",
                             abf="abc",
                             bbb=123, # Works
                             cdb=b'0x\0x\1x') # Also works

bad_type_hint_db: Storage[str, str, int] = Storage("string_again",
                                           abc=123, # Fine
                                           whoops=3.14159) # A type checker like Pyright will flag this

print(bad_type_hint_db["whoops"]) # still accessible though, as type hints do not affect execution as a whole

default_db: Storage = Storage("last_string", foo="bar", fah="hah") # Functionally `Storage[str, str, Any]` or `dict[str, dict[str, Any]]`
```

---

#### `Storage.to_dict()`

```py
def to_dict(self) -> dict[str, dict[str, Any]]
```

Return the `Storage` instance represented as a nested dict `{top_level_key: {subkey: value}}`. **Use this method as a fallback if `dict(Storage)` ever fails.**

##### Arguments
- None

##### Outputs
- `dict[str, dict[str, Any]]` — dict representation of the `Storage` instance.

##### Examples
```py
db = Storage("users", alice="id1")
print(db.to_dict())  # {"users": {"alice": "id1"}}
```

---

#### `Storage.keys()`

```py
def keys(self) -> KeysView[Any]
```

Return a `dict_keys` object (internally `collections.abc.KeysView`, see [PEP 3106](https://peps.python.org/pep-3106/)) for the top-level key (helper to make `dict(Storage)` possible).

##### Arguments
- None

##### Outputs
- `KeysView[Any]` — view containing the top-level key.

##### Examples
```py
db = Storage("k", a=1)
print(list(db.keys()))  # ["k"]
```

### Special Methods

#### `__getitem__`

```py
def __getitem__(self, key: str | int | slice) -> Any
```

- If `key` equals the top-level key returns the values dict; if `str` returns the subvalue; if `int` returns subvalue by index; if `slice` returns a list of values.

##### Examples
```py
db = Storage("s", a=1, b=2)
print(db["a"])      # 1
print(db[0])        # value of first subkey
print(db["s"])      # {'a': 1, 'b': 2}
```

---

#### `__setitem__`

```py
def __setitem__(self, key: str | int, value: Any) -> None
```

- Set subkey by name or set value by integer index.

##### Examples
```py
db["c"] = 3
db[0] = "new"   # replace value at index 0
```

---

#### `__delitem__`

```py
def __delitem__(self, key: str | int | slice) -> None
```

- Delete subkey by name, or by index/slice.

##### Examples
```py
del db["a"]
del db[0]
nonexistent = db["a"] # KeyError
```

---

#### `__len__`

```py
def __len__(self) -> int
```

- Returns number of subkeys.

##### Examples
```py
len(db)  # number of subkeys
```

---

#### `__contains__`

```py
def __contains__(self, item: Any) -> bool
```

- Membership in subkeys.

##### Examples
```py
if "alice" in db:
    print("Alice is in the database!")
```

---

#### `__iter__`

```py
def __iter__(self) -> Generator[str | uuid.UUID | dict[str, Any], None, None]
```

- Yields top-level key first, then each `{subkey: value}` as single-item dicts.

##### Examples
```py
for item in db:
    print(item)
```

---

#### Operator behaviors

> [!important]
> `Storage` uses `functools.total_ordering` to auto-complete certain comparison methods.

- `__add__(self, other: Storage | dict[str, Any] | list[Any]) -> Storage` — merges values (warnings on non-Storage inputs).
- `__sub__(self, other: Storage | dict[str, Any]) -> Storage` — subtraction based on overlapping keys.
- `__truediv__(self, other: Storage | dict | int) -> Storage | list[Storage]` — with `int`: split into equal parts; with `Storage`/`dict`: performs subtraction logic.
- `__and__`, `__or__`, `__xor__` — set-like intersection/union/symmetric-difference of subkeys; often return `Storage` or `0` if empty.
- `__eq__`, `__lt__`, `__le__` — comparisons between `Storage` and other `Storage`s / `dicts`. With `functools.total_ordering`, `__ge__` and `__gt__` are autocompleted.
- `__lshift__`, `__rshift__` — slice-like operations by index.
- Comparison dunders follow `total_ordering` semantics with key-matching restrictions.

##### Examples
```py
a = Storage("k", foo=1, bar=2)
b = Storage("k", baz=3, bar=9)
c = a | b   # union -> Storage with foo, bar, baz
d = a & b   # intersection -> Storage with bar only
parts = a / 2  # splits into list of Storage containing two equal sections of it (if length divisible)
```

---

#### `Storage.__enter__()` / `Storage.__exit__()`

```py
def __enter__(self) -> dict

def __exit__(self,
           exc_type: type[BaseException] | None,
           exc_val: BaseException | None,
           exc_tb: TracebackType | None
          ) -> bool
```

Use `Storage` in a `with`-statement. Preferred over deprecated `auto_delete_self` behavior. **Will be refined in kms-semver2.0.0.**

##### Arguments
- `__enter__`: none
- `__exit__`: standard context manager exception params

##### Outputs
- `__enter__`: returns `dict(self.values)`
- `__exit__`: returns `True` on success; prints info on errors and returns `False` to propagate exceptions.

##### Examples
```py
with Storage("tmp", a=1, b=2) as data:
    # data is dict of values
    print(data)
```

### Other Info

- `auto_delete_self` class attribute and `instant_delete` argument to `store()` are deprecated — prefer `with Storage(...)` usage.
- Format specifiers `.tuplef` and `.tuplet` are deprecated and will be removed in v2.0.
- **As of `kms-semver1.3.1`, you can do the following:**
	- Cast any `Storage` instance into a `dict` using the `dict()` constructor
	- Type-hint `Storage`with the subscription format `Storage[TopKey, SubKey, SubVal]`

## `Storage.Load`

### Methods

#### `Storage.Load.by_key()`

```py
@classmethod
def by_key(cls,
           file_path: str,
           key: Any,
           raw: bool=False
          ) -> Storage | None:
```

Load a json file and find the key to extract
a single key-multivalue pair and its values.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`key`|`Any`|Required|Top-level key to search for (strings recommended).|
|`raw`|`bool`|`False`|If `False` attempt to decode encoded values; if `True` return raw stored values.|

##### Output

- `Storage`: Returns a Storage object containing the loaded data if found.
- `None`: Returns None if the key was not found or if there was an error.

##### Example

```py
s = Storage.Load.by_key("db.json", "users")
print(repr(s))
```

---

#### `Storage.Load.by_index()`

```py
@classmethod
def by_index(cls,
             file_path: str,
             index: int,
             raw: bool=False
            ) -> Storage | None:
```

Load a json file and find the index at which to
extract a single key-multivalue pair and its values.

Do note that this method bases the start index at 0.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`index`|`int`|Required|0-based index of top-level key to return.|
|`raw`|`bool`|`False`|If `False` attempt to decode encoded values; if `True` return raw stored values.|

##### Returns

- `Storage`: If sucessful, a Storage object will be returned with the loaded data.
- `None`: Only returned on failure to load the file or if the index is out of bounds.

##### Example

```py
```

---

#### `Storage.Load.keys()`

```py
@classmethod
def keys(cls,
         file_path: str
        ) -> list[str] | None:
```

Load a json file and returns the keys of that file.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|

##### Returns
- `list[str]`: A list containing strings of the top level keys in the loaded JSON file.
- `None`: May return None on error or if no keys were found.

##### Example

```py
```

---

#### `Storage.Load.values()`

```py
@classmethod
def values(cls,
           file_path: str,
           key: Any,
           keys: bool=False,
           raw: bool=True
          ) -> list[str] | None:
```

Loads a json file and returns the values under the inputed key.

Unlike other loading methods, this one returns the raw values by default.

Keys can also be returned as a key-value pair if keys=True.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`key`|`Any`|Required|Top-level key to fetch values for.|
|`keys`|`bool`|`False`|If `True`, returns `["prop: value", ...]` strings; otherwise returns list of values.|
|`raw`|`bool`|`True`|If `True`, return raw stored values (no decode). If `False`, attempt to decode encoded ints.|

##### Returns
- `list[str]`: A list containing the values under the specified key in the loaded data. If `keys=True`, then the list will contain key-value pairs in the format "key: value".
- `None`: Returns None if the key was not found or if there was an error.

##### Example

```py
```

### Other Info

- This class cannot be instantiated. Attempting to do so will raise [`kms.NoInstantiationError`](#kmsnoinstantiationerror).
- Aside from `Storage`, this is the only class with [a] method(s) that return(s) a `Storage` object.

## `Storage.Edit`

### Methods

#### `Storage.Edit.propkey()`

```py
@classmethod
def propkey(cls,
            file_path: str,
            top_lv_key: Any,
            oldpropkey: str,
            newpropkey: str,
            noexist_ok: bool=True
           ) -> None
```

Rename a subkey within a top-level key.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----:|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`top_lv_key`|`Any`|Required|Top-level key (recommended `str`).|
|`oldpropkey`|`str`|Required|Existing subkey to rename.|
|`newpropkey`|`str`|Required|New name for the subkey.|
|`new`|`bool`|`True` (DEPRECATED)|Deprecated alias for `noexist_ok`.|
|`noexist_ok`|`bool`|`True`|If `True`, create `newpropkey` with empty value when `oldpropkey` missing; otherwise raise `KeyNotFoundError`.|

##### Outputs
- `None`. `KeyNotFoundError` may be raised if any key is not found.

##### Examples
```py
Storage.Edit.propkey("db.json", "users", "username", "user_name")
```

---

#### `Storage.Edit.propval()`

```py
@classmethod
def propval(cls,
            file_path: str,
            top_lv_key: Any,
            propkey: str,
            newval: str
           ) -> None
```

Changes the value for an existing subkey under a top-level key.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----:|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`top_lv_key`|`Any`|Required|Top-level key (recommended `str`).|
|`propkey`|`str`|Required|Subkey whose value will be changed.|
|`newval`|`str`|Required|New value for the subkey.|

##### Outputs
- `None`. Raises `KeyNotFoundError` if top-level key missing.

##### Examples
```py
Storage.Edit.propval("db.json", "users", "alice", "new-id")
```

---

#### `Storage.Edit.key()`

```py
@classmethod
def key(cls, file_path: str, oldkey: Any, newkey: Any) -> None
```

Renames any top-level key in the JSON file; values stay unchanged.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----:|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`oldkey`|`Any`|Required|Existing top-level key to rename.|
|`newkey`|`Any`|Required|New top-level key name.|

##### Outputs
- `None`. Raises `KeyNotFoundError` if `oldkey` missing.

##### Examples
```py
Storage.Edit.key("db.json", "users", "accounts")
```

### Other Info

- This class cannot be instantiated. Attempting to do so will raise [`kms.NoInstantiationError`](#kmsnoinstantiationerror).

## `Storage.Delete`

### Methods

#### `Storage.Delete.by_propkey()`

```py
@classmethod
def by_propkey(cls,
               file_path: str,
               top_lv_key: Any,
               property_key: str
              ) -> None
```

Delete a subkey inside a top-level key.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`top_lv_key`|`Any`|Required|Top-level key (recommended `str`).|
|`property_key`|`str`|Required|Subkey to delete.|

##### Outputs
- `None`. Raises `KeyNotFoundError` if key or property missing.

##### Examples
```py
Storage.Delete.by_propkey("db.json", "users", "temp")
```

---

#### `Storage.Delete.by_key()`

```py
@classmethod
def by_key(cls, file_path: str, key: Any) -> None
```

Delete a top-level key (and its subkeys) entirely from the JSON file.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`key`|`Any`|Required|Top-level key to delete.|

##### Outputs
- `None`. Raises `KeyNotFoundError` if key missing.

##### Examples
```py
Storage.Delete.by_key("db.json", "old_key")
```

---

#### `Storage.Delete.all()`

```py
@staticmethod
def all(file_path: str, warn: bool=True) -> None
```

Delete all data in the JSON file (overwrite with `{}`). Shows a `DeleteWarning` unless `warn=False` or the `DeleteWarning` is being ignored via `warnings` filters.

##### Arguments

| Symbol | Type Hint | Default | Description |
|----|----|----|----|
|`file_path`|`str`|Required|Path to JSON file.|
|`warn`|`bool`|`True`|If `True` show a `DeleteWarning` before deleting. If `False`, skip the warning. Ignoring `DeleteWarning` via `warnings.filterwarnings` also suppresses the prompt.|

##### Outputs
- `None`.

##### Examples
```py
# Normal run: warns
Storage.Delete.all("db.json")

# To force without warning:
Storage.Delete.all("db.json", warn=False)

# Or, filter out the warning to skip warn
import warnings, key_multivalue_storage as kms

warnings.filterwarning(action='ignore', category=kms.DeleteWarning)
Storage.Delete.all("db.json") # Works just like when warn is set to False!
```

### Other Info

- This class cannot be instantiated. Attempting to do so will raise [`kms.NoInstantiationError`](#kmsnoinstantiationerror).

# Custom Warnings and Exceptions

> [!warning]
> From kms-semver1.3.0 onward, the usage of `kms.Storage.<warning or exception>` has been deprecated. Please use the format `kms.<warning or exception>` instead.

## Warnings

Custom warnings for `kms` are stored in the `utils.warnings` module.

### `kms.DeleteWarning`

**Inherits from:** `UserWarning`

> Warns you about deleting all contents of a database file.

### `kms.AdditionFailureWarning`

**Inherits from:** `RuntimeWarning`

> Warns you when attempting to add a Storage instance and a dictionary or list.

### `kms.SubtractionFailureWarning`

**Inherits from:** `RuntimeWarning`

> Warns you when attempting to subtract a Storage instance by a dictionary, and vice versa.
> 
> Also applies to division, despite the name.

### `kms.CastWarning`

**Inherits from:** `UserWarning`

> Warns you about attempting to pass a key argument as something other than a string.

## Exceptions

Custom exceptions for `kms` are stored in the `utils.exceptions` module.

#### `kms.KeyNotFoundError`

**Inherits from:** `KeyError`

> Custom exception raised when a key is not found.

**Example**: if attempting to search for a nonexistent key with
`Storage.Load.by_key`, this would be raised.

#### `kms.NoInstantiationError`

**Inherits from:** `TypeError`

> Custom exception raised when attempting to instantiate a
non-instantiable class.

**Example**: if attempting to instantiate a helper class like `Load`,
this would be raised.
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlszNzgyNTM5NzQsMTUyNDA1MzEw
MCwxNjYxMTc4MTI2LC0xOTkwNzY4MDYsMjE0MDM3ODY2MSwxNj
E5NzYyMzQ2LDQzNzE4ODI3NCwxNjI4MDMwODcyXX0=
-->