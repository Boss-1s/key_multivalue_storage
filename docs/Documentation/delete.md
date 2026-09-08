> [!note]
> Note that each main class and module **has a help() method**, accessible via `<class/module>.help()`. These `help()` methods are simply docstring printers and hinters, so they will not be touched on in this documentation.


| [<< Back](./edit) (*`edit.py`*) | [Next >>](./utils) (*`utils/`*) |
| :--------: | :---------: |
| | |
{: style="display: flex; justify-content: center; width: 100%;"}

# `delete.py`

This module houses the `Delete` class. As the 'Grim Reaper' of the library, it removes objects stored in a JSON file via `Storage.store()`.

## Structure of the Module

> [!tip]
> Click on a class or method below to go straight to its documentation!

- `delete.py` — deletion helpers (Delete class)
	- [`Delete`](#storagedelete)
		- [`by_key`](#storagedeleteby_key)
		- [`by_propkey`](#storagedeleteby_propkey)
		- [`all`](#storagedeleteall)

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

##### Example
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

##### Example
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

##### Example
```py
# Normal run: warns
Storage.Delete.all("db.json")

# To force without warning:
Storage.Delete.all("db.json", warn=False)

# Or, filter out the warning to skip warn
import warnings, key_multivalue_storage as kms

warnings.filterwarning(action='ignore', category=kms.DeleteWarning)
Storage.Delete.all("db.json") # Works just like when warn is set to False
```

### Other Info

- This class cannot be instantiated. Attempting to do so will raise [`kms.NoInstantiationError`](#kmsnoinstantiationerror).
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlsyMTA3MjA2NDEyXX0=
-->