
| [<< Back](./warnings) (*`utils/warnings.py`*) | [Return >>](..#structure-of-the-library) (*to Documentation*) |
| :--------: | :---------: |
| | |
{: style="display: flex; justify-content: center; width: 100%;"}

# `utils/exceptions.py`

Custom exceptions for `kms` are stored in the `utils.exceptions` module, relative path `./utils/exceptions.py`.

## Structure of the Module

> [!tip]
> Click on a class or method below to go straight to its documentation!

- `exceptions.py`       — custom exceptions
	- [`KeyNotFoundError`](#kmskeynotfounderror)
	- [`NoInstantiationError`](#kmsnoinstantiationerror)

## Classes

> [!warning]
> From kms-semver1.3.0 onward, the usage of `kms.Storage.<warning or exception>` has been deprecated. Please use the format `kms.<warning or exception>` instead.

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
BnZm1cbiIsImhpc3RvcnkiOlstMTU0MzgxNjg2MiwtMTIwNDU2
OTgyOF19
-->