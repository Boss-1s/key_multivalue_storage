
| [<< Back](../delete) (*`delete.py`*) | [Next >>](warnings) (*`utils/warnings.py`*) |
| :--------: | :---------: |
| | |
{: style="display: flex; justify-content: center; width: 100%;"}

# `utils/`

> [!warning]
> From kms-semver1.3.0 onward, the usage of `kms.Storage.<warning or exception>` has been deprecated. Please use the format `kms.<warning or exception>` instead.

## `__init__.py`

This submodule does not contain an `__init__.py`. This means that you cannot import from `key_multivalue_storage.utils`, but must specify the module name.

```py
# Works!
from key_multivalue_storage import warnings
# Works; kms-semver1.3.0 exposed all warnings and exceptions to top level
from key_multivalue_storage import CastWarning

# ERROR: cannot resolve symbol NoInstatiationError of module utils
from key_multivalue_storage.utils import NoInstatiationError

# Works -- you must specify the module; in this case, exceptions.
from key_multivalue_storage.utils.exceptions import NoInstantiationError
```

## Structure of the Submodule

> [!tip]
> Click on a module, class, or method below to go straight to its documentation!

- `utils/`
	- [`exceptions.py`](exceptions)       — custom exceptions
		- [`KeyNotFoundError`](exceptions#kmskeynotfounderror)
		- [`NoInstantiationError`](exceptions#kmsnoinstantiationerror)
	- [`warnings.py`](warnings)         — custom warning classes and private warning decorators
		- [`DeleteWarning`](warnings#kmsdeletewarning)
		- [`CastWarning`](warnings#kmscastwarning)
		- [`AddtionFailureWarning`](warnings#kmsadditionfailurewarning)
		- [`SubtractionFailureWarning`](warnings#kmssubtractionfailurewarning)
<!--stackedit_data:
eyJwcm9wZXJ0aWVzIjoiZXh0ZW5zaW9uczpcbiAgcHJlc2V0Oi
BnZm1cbiIsImhpc3RvcnkiOlsxNTM3MTQ3NTZdfQ==
-->