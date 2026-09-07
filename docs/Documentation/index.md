
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

> [!tip]
> Click on a module, class, or method below to go straight to its documentation!

- `src/key_multivalue_storage/`
  - [`storage.py`](storage) — main Storage class (core functionality)
	  - [`Storage`](storage#storage)
		  - [`__init__`](storage#arguments)
		  - [`store`](storage#storage-store)
		  - [`keys`](storage#storage-keys)
		  - [`to_dict`](storage#storage-to-dict)
  - [`load.py`](load) — loading helpers (Load class)
	  - [`Load`](load#storage-load)
		  - [`by_key`](load#storage-load-by-key)
		  - [`by_index`](load#storage-load-by-index)
		  - [`keys`](load#storage-load-keys)
		  - [`values`](load#storage-load-values)
  - [`edit.py`](edit) — editing helpers (Edit class)
	  - [`Edit`](edit#storage-edit)
		  - [`propkey`](edit#storage-edit-propkey)
		  - [`propval`](edit#storage-edit-propval)
		  - [`key`](edit#storage-edit-key)
  - [`delete.py`](delete) — deletion helpers (Delete class)
	  - [`Delete`](delete#storage-delete)
		  - [`by_key`](delete#storage-delete-by-key)
		  - [`by_propkey`](delete#storage-delete-by-propkey)
		  - [`all`](delete#storage-delete-all)
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
BnZm1cbiIsImhpc3RvcnkiOlsxNDIzNjM2NTMyXX0=
-->