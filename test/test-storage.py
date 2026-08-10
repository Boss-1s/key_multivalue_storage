"""
test-general-v1.3.py - A better general test file for kms, designed
specifically for the new `semver1.3.x` update series in mind.

Compatible versions for this test file: >=kms-v1.3.0/2026.07.30

for semver1.2.x, use the original 'test-general.py' file instead.
"""
import json
import os
from typing import Any

from key_multivalue_storage.storage import Storage
from key_multivalue_storage.load import Load
from key_multivalue_storage.edit import Edit
from key_multivalue_storage.delete import Delete

print("Begin test for semver1.3.x")

Delete.all("test_storage.json", warn=False)

print("Part 1: Storage instantiation and type hinting")

normal_db = Storage("top_lv_key", foo="bar", baz="qux")

will_be_deleted_db = Storage("i_will_be_deleted", foo="bar", baz="qux")

bad_str_db = Storage(1234, foo="bar", baz="qux")

assert isinstance(bad_str_db.key, str)

#pylint: disable=unused-variable
type_hint_db: Storage[str, str, str|int] = Storage("top_lv_key", foo="bar", baz=123)

#pylint: disable=unused-variable, line-too-long
bad_type_hint_db: Storage[str, str, str|int] = Storage("top_lv_key", foo="bar", baz=3.14) #type: ignore

print("Part 1 passed.")
del type_hint_db
del bad_type_hint_db
print("Part 2: Storage - global attributes")

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

print("Part 2 passed.")
print("Part 3: Storage() instance attributes")

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

print("Part 3 passed.")
print("Part 4: Storage() instance methods")
# NOTE: This excludes help(), which is covered by test-meta.

normal_db.store("test_storage.json")

with open("test_storage.json", 'r', encoding='utf-8') as f:
    store: dict[str, dict[str, Any]] = json.loads(f.read())

assert isinstance(store, dict)
assert store != dict(normal_db)

# DEPRECATED: deprecated test here...
will_be_deleted_db.store("test_storage.json",
                         instant_delete=will_be_deleted_db.auto_delete_self,
                         indent=4, encode=True)

bad_str_db.store("test_storage.json", indent=4)

# INFO: using json.load because kms.Load should be a seperate sectional test
with open("test_storage.json", 'r', encoding='utf-8') as f:
    store: dict[str, dict[str, Any]] = json.loads(f.read())

assert isinstance(store, dict)
assert dict(bad_str_db).items() <= store.items()

normal_db.store("temp_storage.json", encode=False)

with open("temp_storage.json", 'r', encoding='utf-8') as f:
    store: dict[str, dict[str, Any]] = json.loads(f.read())

assert {normal_db.key: normal_db.values} == store

os.remove("temp_storage.json")

assert normal_db.key in normal_db.keys()
assert bad_str_db.key in bad_str_db.keys()

assert isinstance(normal_db.to_dict(), dict)
assert isinstance(bad_str_db.to_dict(), dict)

print("Part 4 passed.")

del normal_db
del will_be_deleted_db
del bad_str_db

print("Part 5: Dunder Methods")

db: Storage[str, str, Any] = Storage("key", foo="bar")

assert str(db) # __str__
assert repr(db) # __repr__

# __eq__ #

assert db == Storage("key", foo="bar")

# NOTE: other __eq__ with dict is handled by an issue-patch test

# __lt__ #

try:
    db < Storage("different_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Why can Storage be compared when top level keys are different...?"

assert not db < Storage("key", foo='bar')
assert db < Storage("key", foo="bar", baz="qax")

# __le__ #

assert db <= Storage("key", foo="bar")
assert db <= Storage("key", foo="bar", baz="qax")

# __add__ #

try:
    db + Storage("different_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Why can Storages be added when top level keys are different...?"

new_db = db + Storage("key", baz="qax", default="lorem ipsum")

assert isinstance(new_db, Storage)
assert 'default' in new_db.values
assert new_db['default'] == 'lorem ipsum'
assert new_db['baz'] == 'qax'
assert new_db['foo'] == db['foo']

dict_db = db + new_db.values

assert isinstance(dict_db, Storage)
assert 'default' in dict_db.values
assert dict_db['default'] == 'lorem ipsum'
assert dict_db['baz'] == 'qax'
assert dict_db['foo'] == db['foo'] == new_db['foo']

list_db = db + ['qax', 'foo', 'lorem ipsum']

assert isinstance(list_db, Storage)
assert isinstance(list_db['undefined'], list)
assert list_db['undefined'] == ['qax', 'foo', 'lorem ipsum']

# __radd__ #

dict_db_r = new_db.values + db
assert dict_db_r == dict_db

del new_db, dict_db, dict_db_r, list_db

# __call__ #

db(a="b", c="d", e='f')

# __sub__ #

try:
    db - Storage("different_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Why can Storages be subtracted when top level keys are different...?"

new_db = Storage("key", foo="bar", baz="qax") - db

assert isinstance(new_db, Storage)
assert 'baz' in new_db.values
assert new_db['baz'] == 'qax'
try:
    new_db['foo']
except KeyError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "the foo=bar pair should have been deleted by subtraction!"

dict_db = db - {'e': 'f'}

assert isinstance(dict_db, Storage)
assert 'a' in dict_db.values
assert dict_db['a'] == 'b'
assert dict_db['c'] == 'd'
try:
    dict_db['e']
except KeyError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "the e=f pair should have been deleted by subtraction!"

# __rsub__ #

dict_db_r = {'e': 'f'} - db
assert dict_db_r == dict_db

assert dict(db) == {
    "key": {
        'a': 'b',
        'c': 'd',
        'e': 'f',
        'foo': 'bar'
    }
}, f"the original variable db (current value `{db}`) should NOT have changed..."

del new_db, dict_db, dict_db_r

# __truediv__ / __rtruediv__ #

db = Storage("key", foo="bar", baz='qax') # Reassign or else i will be vewy confused

db1 = Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")
db2 = dict(Storage("key", foo="bar", baz="qax", c="d", g="h", i="j").values)
db3 = Storage("key", a='b', e='f')

db4 = db1 / db2

assert db3 == db4 == (db1 - db2)
assert db1 == Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")

db5 = db1 / 2

assert len(db5) == 2

for storage in db5:
    assert len(storage.values) == 3

assert db5[0] == Storage("key", foo="bar", baz="qax", a="b")
assert db5[1] == Storage("key", c="d", e="f", g="h")

assert db1 == Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")

db5 = db1 / 1

assert len(db5) == 1
assert db1 == db5[0]

try:
    db1 / 0.5 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "You shuold not be able to divide a Storage by a float..."

try:
    2 / db1 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "You shuold not be able to divide an int by a Storage..."

db2 = dict(Storage("key", foo="bar", baz="qax", c="d", g="h", i="j").values)

db4 = db2 / db1

assert db3 == db4
assert db1 == Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")

try:
    db1 / 10000
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Storage length of 6 is not divisible by 10,000 (cannot be greater than 9)"

try:
    db1 / 7
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Storage length of 6 is not divisible by 7 (cannot be float)"

del db1, db2, db3, db4, db5

os.remove("test_storage.json")
