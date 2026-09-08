> [!note]
> Note that each main class and module **has a help() method**, accessible via `<class/module>.help()`. These `help()` methods are simply docstring printers and hinters, so they will not be touched on in this documentation.

| [<< Back](./load) (*`load.py`*) | [Next >>](./delete) (*`delete.py`*) |
| :--------: | :---------: |
| | |
{: style="display: flex; justify-content: center; width: 100%;"}

# `edit.py`

This module houses the class `Edit`. Despite being implemented a bit later than the other helper classes, this one is just as equally as important, as it allows remote editing of JSON data stored with [`Storage.store()`](/key_multivalue_storage/Documentation/storage#storage-store).

## Structure of the Module

> [!tip]
> Click on a class or method below to go straight to its documentation!

- `edit.py` — editing helpers (Edit class)
	- [`Edit`](#storageedit)
	  - [`propkey`](#storageeditpropkey)
	  - [`propval`](#storageeditpropval)
	  - [`key`](#storageeditkey)

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

##### Example
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

##### Example
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

##### Example
```py
Storage.Edit.key("db.json", "users", "accounts")
```

### Other Info

- This class cannot be instantiated. Attempting to do so will raise [`kms.NoInstantiationError`](#kmsnoinstantiationerror).
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlsxODUxMTk3MDU1XX0=
-->