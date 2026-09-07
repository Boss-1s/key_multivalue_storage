> [!note]
> Note that each main class and module **has a help() method**, accessible via `<class/module>.help()`. These `help()` methods are simply docstring printers and hinters, so they will not be touched on in this documentation.

# `storage.py`

Main module housing the most important class in `kms`: `Storage`.

## Structure of the Module

- `storage.py` — main Storage class (core functionality)
	- [`Storage`](#storage)
		- [`__init__`](#arguments)
		- [`store`](#storage-store)
		- [`keys`](#storage-keys)
		- [`to_dict`](#storage-to-dict)
		- [Special methods](#special-methods)

## `Storage`
The `Storage` class is the main class in this library, in which all operations revolve around. It is (so far) the only class in the library that can be instantiated.

### Arguments
- `key: Any` - Represents the **top level key** of the Storage object. Recommended to be a string, however, it is type `Any` to allow for a broader range of choices.
- `**kwargs: Any` - The keyword arguments that are converted into the instance variable `values`. It is, in technicality, a `dict[str, Any]`.

> [!important]
> These two parameters make the Storage object's default type to be `dict[str, dict[str, Any]]`. However, by [type-hinting Storage specifically](#type-hinting), you can change that.

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

##### Example

```py
db = Storage("settings", theme="dark", timeout=30)
db.store("config.json")            # writes config.json
db.store("config", encode=True)    # will append .json -> config.json and encode values
```

---

#### `Storage.to_dict()`

```py
def to_dict(self) -> dict[str, dict[str, Any]]
```

Return the `Storage` instance represented as a nested dict `{top_level_key: {subkey: value}}`.

> [!warning]
> **Only use this method as a fallback if `dict(Storage)` ever fails.**

##### Arguments
- None

##### Outputs
- `dict[str, dict[str, Any]]` — dict representation of the `Storage` instance.

##### Example
```py
db = Storage("users", alice="id1")
print(db.to_dict())  # {"users": {"alice": "id1"}}
```

---

#### `Storage.keys()`

```py
def keys(self) -> KeysView[Any]
```

Return a `dict_keys` object (internally `collections.abc.KeysView`, see [PEP 3106](https://peps.python.org/pep-3106/)) for the top-level key.

##### Arguments
- None

##### Outputs
- `KeysView[Any]` — view containing the top-level key.

##### Example
```py
db = Storage("k", a=1)
print(list(db.keys()))  # ["k"]
```
---

### Special Methods

#### `__getitem__`

```py
    @overload
    def __getitem__(self, key: TopKey) -> dict[SubKey, SubVal]: ...

    @overload
    def __getitem__(self, key: SubKey) -> SubVal: ...

    @overload
    def __getitem__(self, key: int) -> SubVal: ...

    @overload
    def __getitem__(self, key: slice) -> list[SubVal]: ...


def __getitem__(self, key: str | int | slice) -> Any
```
- If `key` equals the top-level key returns the values dict; if `str` returns the subvalue; if `int` returns subvalue by index; if `slice` returns a list of values.

##### Overloads

| Argument | Overload type | Overload return | Description
| :---: | :---: | :---: | --- |
| `key` | `TopKey` (`str`) | `dict[SubKey, SubVal]` (`self.values`) | When passing the top-level key for `key`, `self.values` will be returned. |
| `key` | `SubKey` (`str`) | `SubVal` (`self.values[key]`) | When passing any existing subkey for `key`, its corresponding value will be returned. |
| `key` | `int` | `SubVal` (`self.values.values()[key]`) | When passing an integer for `key`, the value of the index of the subkey in `list(self.values.keys())` is returned. ***Note*: In `kms-semver2.0.0`, this may be changed to return a key-value pair OR removed completely to mimic `dict`.** |
| `key` | `slice` | `list[SubVal]` (`list(self.values.values())[key]`) | When passing a slice object (`[start:stop]`) to `key`, a list of the value od the index of the subkey in `list(self.values.keys())` is returned. ***Note*: In `kms-semver2.0.0`, this may be changed to return key-value pairs OR removed completely to mimic `dict`.** |

##### Example
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

##### Example
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

##### Example
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

##### Example
```py
len(db)  # number of subkeys
```

---

#### `__contains__`

```py
def __contains__(self, item: Any) -> bool
```

- Membership in subkeys.

##### Example
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

##### Example
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

##### Example
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

##### Example
```py
with Storage("tmp", a=1, b=2) as data:
    # data is dict of values
    print(data)
```

---

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

#### Example

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

### Other Info

- `auto_delete_self` class attribute and `instant_delete` argument to `store()` are deprecated — prefer `with Storage(...)` usage.
- Format specifiers `.tuplef` and `.tuplet` are deprecated and will be removed in v2.0.
- **As of `kms-semver1.3.1`, you can do the following:**
	- Cast any `Storage` instance into a `dict` using the `dict()` constructor
	- Type-hint `Storage`with the subscription format `Storage[TopKey, SubKey, SubVal]`
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlsyMjkxMjgwNDRdfQ==
-->