---
title: Documentation
sidebar_type: toc
---

# Documentation - Home

> [!Note]
> **To use this library, you must have Python installed on your device.**
>
> *Don't have Python? Install it here: https://python.org/downloads*

## Installation
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

## Basic Usage
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

## Structure of the Library

> [!note]
> Certain items that aren't part of the public API and/or are part of repo systems like workflows are not shown here.

> [!tip]
> **Click on a module, class, or method below to go straight to its documentation!**

- `src/key_multivalue_storage/`
  - [`storage.py`](storage) — main Storage class (core functionality)
	  - [`Storage`](storage#storage)
		  - [`__init__`](storage#arguments)
		  - [`store`](storage#storagestore)
		  - [`keys`](storage#storagekeys)
		  - [`to_dict`](storage#storageto_dict)
  - [`load.py`](load) — loading helpers (Load class)
	  - [`Load`](load#storageload)
		  - [`by_key`](load#storageloadbykey)
		  - [`by_index`](load#storageloadby_index)
		  - [`keys`](load#storageloadkeys)
		  - [`values`](load#storageloadvalues)
  - [`edit.py`](edit) — editing helpers (Edit class)
	  - [`Edit`](edit#storageedit)
		  - [`propkey`](edit#storageeditpropkey)
		  - [`propval`](edit#storageeditpropval)
		  - [`key`](edit#storageeditkey)
  - [`delete.py`](delete) — deletion helpers (Delete class)
	  - [`Delete`](delete#storagedelete)
		  - [`by_key`](delete#storagedeleteby_key)
		  - [`by_propkey`](delete#storagedeleteby_propkey)
		  - [`all`](delete#storagedeleteall)
  - [`utils/`](utils)
    - [`exceptions.py`](utils/exceptions)       — custom exceptions
	    - [`KeyNotFoundError`](utils/exceptions#kmskeynotfounderror)
	    - [`NoInstantiationError`](utils/exceptions#kmsnoinstantiationerror)
    - [`warnings.py`](utils/warnings)         — custom warning classes and private warning decorators
	    - [`DeleteWarning`](utils/warnings#kmsdeletewarning)
	    - [`CastWarning`](utils/warnings#kmscastwarning)
	    - [`AddtionFailureWarning`](utils/warnings#kmsadditionfailurewarning)
	    - [`SubtractionFailureWarning`](utils/warnings#kmssubtractionfailurewarning)
    - *`metadata.py`*
- _`test/`_
  - _`test-storage.py`_ — **Mainstream test targeting `kms.storage`**
  - _`test-load.py`_ — **Mainstream test targeting `kms.load`**
  - _`test-edit.py`_ — **Mainstream test targeting `kms.edit`**
  - _`test-delete.py`_ — **Mainstream test targeting `kms.delete`**
  - _`test-general.py`_ — *legacy, only used to ensure backwards compatibility*
  - _`test-meta.py`_ — **Mainstream test targeting `kms.utils.metadata`**
  - _`test-exceptions.py`_ — **Mainstream test targeting `kms.utils.exceptions` and `kms.utils.warnings`**
  - _`test-fix-*.py` / `test-feat-*.py`_ — Targeted tests from PRs. **Integrated into mainstream tests every minor update**, starting from `kms-semver1.4.x`.

## List of Current Deprecations

> [!important]
> Only public deprecations are included. Deprecations to private methods, modules, or logic are not included.

List of current deprecations, sorted by the version they were deprecated. **All deprecations listed below will be formally removed in `kms-semver2.0.0`.**

### `kms-semver1.3.1`

- **Deprecated format specifiers `.tuplef` and `.tuplet`.**
- Attribute `auto_delete_self` and argument `instant_delete` of `Storage.store()` has been deprecated.

### `kms-semver1.3.0`

* **All metadata variables from `kms-semver1.2.2` were renamed.** *You can still use the old names, however they are no longer recommended for use and will display a `DeprecationWarning` warning.*

| Old name | New name |
| :------: | :------: |
| `VERSION` | `semver` |
| `DATE_VERSION` |`calver` |
| `LAST_UPDATE` | `last_update` |

* In `Storage.Delete.by_propkey`: **the required argument `top_level_key` has been deprecated.** Please use the renamed `top_lv_key` instead. *This change was made to match with other methods with the same parameter.*

```py
Storage.Delete.by_propkey(_,top_lv_key='key')
```

* **All warnings and exceptions will no longer be under `kms.Storage` but rather be under just `kms`.**

```py
import key_multivalue_storage as kms

warnings.filterwarning(category=kms.Storage.DeleteWarning) # Old, will raise DeprecationWarning
warnings.filterwarning(category=kms.DeleteWarning) # New, will work properly
```

### `kms-semver1.2.3`

* **All metadata variables from `kms-semver1.2.2` were renamed.** *You can still use the old names, however they are no longer recommended for use and will display a `DeprecationWarning` warning.*

| Old name | New name |
| :------: | :------: |
| `VERSION` | `semver` |
| `DATE_VERSION` |`calver` |
| `LAST_UPDATE` | `last_update` |

* In `Storage.Delete.by_propkey`: **the required argument `top_level_key` has been deprecated.** Please use the renamed `top_lv_key` instead. *This change was made to match with other methods with the same parameter.*

```py
Storage.Delete.by_propkey(_,top_lv_key='key')
```

### `kms-semver1.2.0`

- **Keyword argument `new` of method [`Storage.Edit.propkey`](/key_multivalue_storage/Documentation/edit#editpropkey) was deprecated in favor of the argument `noexist_ok`.**

[***<< Back to home***](..)
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlstMTk3Mzk1MDY0OCwtNTM0MjU2
MjQ4LC0yOTEwMzI4NTFdfQ==
-->