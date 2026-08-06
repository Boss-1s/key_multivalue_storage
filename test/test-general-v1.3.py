"""
test-general-v1.3.py - A better general test file for kms, designed
specifically for the new `semver1.3.x` update series in mind.

Compatible versions for this test file: >=kms-v1.3.0/2026.07.30

for semver1.2.x, use the original 'test-general.py' file instead.
"""
import json
import os
from tkinter import N
from typing import Any

from key_multivalue_storage.storage import Storage
from key_multivalue_storage.load import Load
from key_multivalue_storage.edit import Edit
from key_multivalue_storage.delete import Delete

print("Begin test for semver1.3.x")

Delete.all("test_storage.json", warn=False)

print("Part 1: Storage")
print("Part 1.1: Storage instantiation and type hinting")

normal_db = Storage("top_lv_key", foo="bar", baz="qux")

will_be_deleted_db = Storage("i_will_be_deleted", foo="bar", baz="qux")

bad_str_db = Storage(1234, foo="bar", baz="qux")

assert isinstance(bad_str_db.key, str)

#pylint: disable=unused-variable
type_hint_db: Storage[str, str, str|int] = Storage("top_lv_key", foo="bar", baz=123)

#pylint: disable=unused-variable, line-too-long
bad_type_hint_db: Storage[str, str, str|int] = Storage("top_lv_key", foo="bar", baz=3.14) #type: ignore

print("Part 1.1 passed.")
del type_hint_db
del bad_type_hint_db
print("Part 1.2: Storage - global attributes")

Storage.auto_delete_self = True
Storage.indent = 4
Storage.encode = False

assert Storage.auto_delete_self is True
assert Storage.indent == 4
assert Storage.encode is False

assert normal_db.auto_delete_self is True
assert will_be_deleted_db.indent == 4
assert bad_str_db.encode is False

normal_db.auto_delete_self = False
normal_db.encode = True

will_be_deleted_db.auto_delete_self = True
will_be_deleted_db.encode = False

bad_str_db.auto_delete_self = False
bad_str_db.encode = False

assert normal_db.auto_delete_self is False
assert normal_db.encode is True

assert will_be_deleted_db.auto_delete_self is True
assert will_be_deleted_db.encode is False

assert bad_str_db.auto_delete_self is False
assert bad_str_db.encode is False

assert Storage.auto_delete_self is True
assert Storage.indent == 4
assert Storage.encode is False

print("Part 1.2 passed.")
print("Part 1.3: Storage() instance attributes")

assert normal_db.key
assert normal_db.values
assert normal_db.instance_id

assert will_be_deleted_db.key
assert will_be_deleted_db.values
assert will_be_deleted_db.instance_id

assert bad_str_db.key
assert bad_str_db.values
assert bad_str_db.instance_id

try:
    # INFO: This SHOULD fail
    Storage.key #type: ignore
except AttributeError:
    print("Storage.key attribute does not exist, as expected.")
except Exception as e:
    raise AssertionError(e) from e
else:
    raise AssertionError("Storage.key attribute exists, but it should not. "+
                         "Are you using the correct version?")

print("Part 1.3 passed.")
print("Part 1.4: Storage() instance methods")
# NOTE: This excludes help(), which is covered by test-meta.

normal_db.store("test_storage.json")

with open("test_storage.json", 'r', encoding='utf-8') as f:
    store: dict[str, dict[str, Any]] = json.loads(f.read())

assert isinstance(store, dict)
# FIXME: After #67 is finished, use the commented code instead
# assert store == dict(normal_db)

# Should fail when == because encoded
assert store != {normal_db.key: normal_db.values}


# FIXME: After #68 is fixed, this should work
# will_be_deleted_db.store("test_storage.json", indent=4, encode=True)

# try:
#     will_be_deleted_db #type: ignore
# except NameError:
#     pass
# else:
#     raise AssertionError()

bad_str_db.store("test_storage.json", indent=4)

# INFO: using json.load because kms.Load should be a seperate sectional test
with open("test_storage.json", 'r', encoding='utf-8') as f:
    store: dict[str, dict[str, Any]] = json.loads(f.read())

assert isinstance(store, dict)
# FIXME: After #67 is finished, use the commented code instead
# assert store == dict(bad_str_db)

assert bad_str_db.key in store.keys()
assert bad_str_db.values in store.values()

normal_db.store("temp_storage.json", encode=False)

with open("temp_storage.json", 'r', encoding='utf-8') as f:
    store: dict[str, dict[str, Any]] = json.loads(f.read())

assert {normal_db.key: normal_db.values} == store

os.remove("temp_storage.json")

print("Part 1.4 passed.")

os.remove("test_storage.json")
