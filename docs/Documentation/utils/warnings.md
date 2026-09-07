# `utils/warnings.py`

Custom warnings for `kms` are stored in the `utils.warnings` module, relative path `./utils/warnings.py`.

## Structure of the Module

- `warnings.py`         — custom warning classes and private warning decorators
	- [`DeleteWarning`](#kmsdeletewarning)
	- [`CastWarning`](#kmscastwarning)
	- [`AddtionFailureWarning`](#kmsadditionfailurewarning)
	- [`SubtractionFailureWarning`](#kmssubtractionfailurewarning)

## Classes

> [!warning]
> From kms-semver1.3.0 onward, the usage of `kms.Storage.<warning or exception>` has been deprecated. Please use the format `kms.<warning or exception>` instead.

### `kms.DeleteWarning`

**Inherits from:** `UserWarning`

> Warns you about deleting all contents of a database file.


### `kms.CastWarning`

**Inherits from:** `UserWarning`

> Warns you about attempting to pass a key argument as something other than a string.

### `kms.AdditionFailureWarning`

**Inherits from:** `RuntimeWarning`

> Warns you when attempting to add a Storage instance and a dictionary or list.

### `kms.SubtractionFailureWarning`

**Inherits from:** `RuntimeWarning`

> Warns you when attempting to subtract a Storage instance by a dictionary, and vice versa.
> 
> Also applies to division, despite the name.
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlsxNDEyODgwMTI4XX0=
-->