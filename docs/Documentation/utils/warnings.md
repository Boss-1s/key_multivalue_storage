
| [<< Back](.) (*`utils/`*) | [Next >>](./edit) (*`utils/exceptions.py`*) |
| :--------: | :---------: |
| | |
{: style="display: flex; justify-content: center; width: 100%;"}

# `utils/warnings.py`

Custom warnings for `kms` are stored in the `utils.warnings` module, relative path `./utils/warnings.py`.

## Structure of the Module

> [!tip]
> Click on a class or method below to go straight to its documentation!

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

Warns you about deleting all contents of a database file.

**Used in:** `Delete.all()`

> [!tip]
> If you ignore this warning, `Delete.all()` will function as if `warn=False` was passed to it!
>
>	```py
>	warnings.filterwarning(action='ignore',
>						   category=kms.DeleteWarning)
>	
>	# Works just like when warn is set to False
>	Storage.Delete.all("db.json")
>	```

---

### `kms.CastWarning`

**Inherits from:** `UserWarning`

Warns you about attempting to pass a key argument as something other than a string.

**Used in:** `Storage`, `Load`, `Edit`, `Delete` - various methods

---

### `kms.AdditionFailureWarning`

**Inherits from:** `RuntimeWarning`

Warns you when attempting to add a Storage instance and a dictionary or list.

**Used in:** `Storage.__add__()`

---

### `kms.SubtractionFailureWarning`

**Inherits from:** `RuntimeWarning`

Warns you when attempting to subtract a Storage instance by a dictionary, and vice versa.

*Also applies to division, despite the name.*

**Used in:** `Storage.__sub__()`, `Storage.__truediv__()`
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOls0MTg2NTA0NDNdfQ==
-->