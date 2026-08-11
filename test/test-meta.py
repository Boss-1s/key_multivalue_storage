"""
test-meta.py - a test file for KMS designed specifaclly to test the new metaclass
and help() method implementations.

Compatible versions for this test file: >=kms-v1.3.0/2026.07.30
"""

import sys
from rich.console import Console
import key_multivalue_storage as kms
from key_multivalue_storage import (
    storage,
    load,
    edit,
    delete
)
from key_multivalue_storage.storage import Storage
from key_multivalue_storage.load import Load
from key_multivalue_storage.edit import Edit
from key_multivalue_storage.delete import Delete
from key_multivalue_storage.utils.metadata import _KmsMeta


print("Begin test\n"+("-"*20)+"\nPart 1: __str__ and __repr__ of class via metaclass\n"+("-"*20))

try:
    print(Storage)
    print(Storage.Load)
    print(Storage.Edit)
    print(Storage.Delete)
except Exception as e:
    raise AssertionError from e

try:
    print(repr(Storage))
    print(repr(Storage.Load))
    print(repr(Storage.Edit))
    print(repr(Storage.Delete))
except Exception as e:
    raise AssertionError from e

assert str(Storage) == repr(Storage)
assert str(Storage.Load) == repr(Storage.Load)
assert str(Storage.Edit) == repr(Storage.Edit)
assert str(Storage.Delete) == repr(Storage.Delete)

print("Part 1 passed.")
print("-"*20)
print("Part 2: help() method for each class")

try:
    kms.help() # Module Help

    storage.help() # storage Module Help
    Storage.help()
    Storage.help(Storage.store)

    load.help()
    Storage.Load.help()
    Storage.Load.help(Storage.Load.keys)

    edit.help()
    Storage.Edit.help()
    Storage.Edit.help(Storage.Edit.propkey)

    delete.help()
    Storage.Delete.help()
    Storage.Delete.help(Storage.Delete.all)

except Exception as e:
    console = Console()
    console.print_exception(show_locals=True)
    console.print(f"[b red]Error: {e}")
    sys.exit(1)

print("Part 2 passed.")
print("-"*20)
print("Part 3: Ensure _KmsMeta can fail correctly")

try:
    class BadMetaClass(metaclass=_KmsMeta): # pylint: disable=unused-variable, too-few-public-methods, line-too-long
        pass
except TypeError as e:
    print(f"Expected TypeError caught: {e}")
except Exception as e:
    raise AssertionError(e) from e

print("Part 3 passed.")
print("-"*20)
print("Part 4: Ensure version properties work")

assert kms.__version__
assert kms.__version_internal__
# -Storage- #
assert Storage.semver
assert Storage.calver
assert Storage.version
assert Storage.last_update
# -DEPRECATED- #
assert Storage.VERSION
assert Storage.LAST_UPDATE
assert Storage.DATE_VERSION
# -Load- #
assert Load.semver
assert Load.calver
assert Load.version
assert Load.last_update
# -Edit- #
assert Edit.semver
assert Edit.calver
assert Edit.version
assert Edit.last_update
# -Delete- #
assert Delete.semver
assert Delete.calver
assert Delete.version
assert Delete.last_update

print("Part 4 passed.")
print("Test file completed successfully.")
