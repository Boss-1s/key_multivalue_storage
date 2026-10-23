import warnings
from rich.markdown import Markdown
from rich.traceback import install
from rich import print
import key_multivalue_storage as kms
from key_multivalue_storage.edit import Edit
from key_multivalue_storage.storage import Storage
from key_multivalue_storage.delete import Delete
from key_multivalue_storage.utils.exceptions import BadBitwiseOperation

install(show_locals=True)

print(f"NextGen is currently {kms.nextgen}")

try:
    kms.test_nextgen()
except TypeError as e:
    print(Markdown(str(e)))
except Exception as e:
    warnings.warn(f"An unexpected exception occurred: {e}")

kms.nextgen = True

kms.test_nextgen()

print(f"NextGen is now {kms.nextgen}")

print("Testing `__enter__`")

with Storage("my_key", foo="bar") as storage:
    assert isinstance(storage, Storage), f"`storage` is type {type(storage)}"
    assert storage["foo"] == "bar"
    assert dict(storage) == {"my_key": {"foo": "bar"}}

print("`__enter__` test passed.")
print("Testing `__iter__`")

for item in (db := Storage("my_key", foo="bar", baz="baq", qux="quux", quuz="corge")):
    assert item != db.key
    assert item in db.values
    assert item not in list(db.values.values())

print("`__iter__` test passed.")
del db
print("Testing BadBitwiseOperation exception")
try:
    raise BadBitwiseOperation("This is a test for BadBitwiseOperation.")
except BadBitwiseOperation as e:
    print(f"Caught expected BadBitwiseOperation: {e}")
except Exception as e:
    assert False, e

kms.nextgen = False

try:
    raise BadBitwiseOperation("This is a test for BadBitwiseOperation.")
except TypeError as e:
    print(f"Caught expected TypeError: {e}")
except Exception as e:
    assert False, e

print("Testing deprecations")

if not kms.nextgen:
    kms.nextgen = True

db = Storage("my_key", foo="bar")

# -- #

try:
    # deprecated since 1.3.1
    db.auto_delete_self # deprecated attr, should not exist in nextgen preview
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

# -- #

kms.nextgen = False

# Deprecated since 1.3.1
tuplef_storage = f"{db:.tuplef}"
tuplet_storage = f"{db:.tuplet}"

kms.nextgen = True

assert tuplef_storage != f"{db:.tuplef}"
assert f"{db:.tuplef}" == repr(db)

assert tuplet_storage != f"{db:.tuplet}"
assert f"{db:.tuplet}" == repr(db)

# -- #

try:
    # deprecated since 1.3.1
    db.auto_delete_self
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # deprecated since 1.3.0
    Storage.VERSION
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # deprecated since 1.3.0
    Storage.LAST_UPDATE
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # deprecated since 1.3.0
    Storage.DATE_VERSION
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.4.0a2
    Storage.Load
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.4.0a2
    Storage.Edit
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.4.0a2
    Storage.Delete
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.3.0
    Storage.DeleteWarning
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.3.0
    Storage.AdditionFailureWarning
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.3.0
    Storage.SubtractionFailureWarning
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # access path deprecated since 1.3.0
    Storage.CastWarning
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

# -- #

try:
    # instant_delete deprecated since 1.3.1
    db.store('test_nextgen.json', instant_delete=True)
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # top_level_key deprecated since 1.2.3/1.3.0
    Delete.by_propkey("test_nextgen.json", top_level_key="my_key", property_key="foo")
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

try:
    # new deprecated since 1.2.0 (oldest deprecation in kms lol)
    Edit.propkey("test_nextgen.json", "my_key", "foo", "baz", new=False)
except TypeError as e:
    pass
except Exception as e:
    raise AssertionError(f"An unexpected exception occurred: {e}") from e

# -And that should be it (for now)!- #
print("All deprecation tests passed.")