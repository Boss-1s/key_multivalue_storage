"""
test-storage.py - A targeted test file for storage.Storage.

Compatible versions for this test file: >=kms-v1.3.1/2026.08.12

for semver1.2.x, use the original 'test-general.py' file instead.
"""
from __future__ import annotations

import json
import os
from types import NotImplementedType
from typing import Any

from rich.console import Console

from key_multivalue_storage.storage import Storage
from key_multivalue_storage.delete import Delete

c = Console()
print = c.print

print("Begin test for semver1.3.x Storage")
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
will_be_deleted_db.store("test_storage",
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
assert db == {"key": {'foo': 'bar'}}

# __lt__ #

try:
    db < Storage("different_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Why can Storage be compared when top level keys are different...?"

assert not db < Storage("key", foo='bar') # pylint: disable=unnecessary-negation
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

multistorage_db = db + {"nested": Storage("key", foo="bar", baz="qax")}

assert isinstance(multistorage_db, Storage)
assert isinstance(multistorage_db['nested'], Storage)
assert multistorage_db['nested'] == Storage("key", foo="bar", baz="qax")

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

del db, db1, db2, db3, db4, db5

## Bitwise Operators ##

db1 = Storage("key", foo="bar", baz='qax') # Reassign or else i will be vewy confused
db2 = Storage("key", foo="bar")
db3 = Storage("key", qwert='yuiop')

# __and__ #

try:
    db1 & Storage("whoops_wrong_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Storage objects with different keys should not be operable..."

db4 = db1 & db2

assert isinstance(db4, Storage)
assert db4 == db2

db4 = db1 & dict(db2.values)

assert isinstance(db4, Storage)
assert db4 == db2

try:
    1000.625 & db1 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "float and Stoarge cannot be operated on with bitwise operator AND"

# __or__ #

try:
    db1 | Storage("whoops_wrong_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Storage objects with different keys should not be operable..."

db4 = db1 | db3

assert isinstance(db4, Storage)
assert db4.values == {'foo': 'bar',
                      'baz': 'qax',
                      'qwert':'yuiop'
}

db4 = db1 | dict(db3.values)

assert isinstance(db4, Storage)
assert db4.values == {'foo': 'bar',
                      'baz': 'qax',
                      'qwert':'yuiop'
}

try:
    1000.625 | db1 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "float and Stoarge cannot be operated on with bitwise operator OR"

# __xor__ #

try:
    db1 ^ Storage("whoops_wrong_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Storage objects with different keys should not be operable..."

db4 = db1 ^ db2

assert isinstance(db4, Storage)
assert db4.values == {'baz': 'qax'}

db4 = db2 ^ db1

assert isinstance(db4, Storage)
assert db4.values == {'baz': 'qax'}

db4 = db1 ^ dict(db2.values)

assert isinstance(db4, Storage)
assert db4.values == {'baz': 'qax'}

try:
    1000.625 ^ db1 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "float and Stoarge cannot be operated on with bitwise operator XOR"

# __lshift__ #

db3(asdfg='hjkl;')

try:
    db1 << db2 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "You shouldn't be able to left-shift Storage with Storage..."

db4 = db3 << 1

assert isinstance(db4, Storage)
assert db4 == Storage("key", asdfg='hjkl;')

db4 = db2 << 1

assert db4 == 0 # INFO: In kms-semver1.x series, Storage cannot be empty

# __rshift__ #

try:
    db1 >> db2 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "You shouldn't be able to left-shift Storage with Storage..."

db4 = db3 >> 1

assert isinstance(db4, Storage)
assert db4 == Storage("key", qwert='yuiop')

db4 = db2 >> 1

assert db4 == 0 # INFO: In kms-semver1.x series, Storage cannot be empty

del db1, db2, db3, db4

# __getitem__ #
# INFO: Since __getitem__ (*bracket notation*) str and self.key overloads have already been used
# like almost everywhere, only `int` and `slice` overloads will be tested

db: Storage[str, str, Any] = Storage(
    "key",
    a=1, # 0
    b=2, # 1
    c=3, # 2
    d=4, # 3
    e=5, # 4
    f=6, # 5
    g=7, # 6
    h=8, # 7
    i=9, # 8
    j=10 # 9
)

assert db[0] == 1
assert db[6] == 7

assert db[8:] == [9, 10]
assert db[1:3] == [2, 3]
assert db[:3] == [1, 2, 3]

fake = db[{'pi': 3.1415926535897932384626}] # type: ignore
assert isinstance(fake, NotImplementedType)

del fake

# __setitem__ #
db['i'] = 987654321

db[9] = 123456789

assert db['i'] == 987654321
assert db[9] == 123456789

# __delitem__ / __len__ / __contains__ #

del db[9]
del db['i']

assert len(db) == 8

assert 'i' not in db
assert 'g' in db

# __iter__ #

iter_list: list[str|dict[str, int]] = []

for item in db:
    iter_list.append(item)

assert iter_list[0] == db.key

del iter_list[0]

for i in range(7):
    assert db[list(iter_list[i].keys())[0]] == db[i] #type: ignore

del iter_list

# __getattr__
try:
    db.encod # type: ignore
except AttributeError:
    c.print_exception()
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "encod is not an attribute of Storage, yet it passes..."


# __enter__ / __exit__ #

db = Storage("key", foo="bar", baz="qax")

with Storage("key", foo="bar", baz="qax") as db_values:
    assert db.values == db_values

try:
    with Storage("key", foo="bar", baz="qax") as db_values:
        assert db.values == db_value # type: ignore # NOSONAR
except NameError:
    pass
except AssertionError:
    assert False
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "no way python thinks that nonexistent variable exists..."

del db_values

# __format__

print(f"Format Specifier .dictf = {db:.dictf}")
print(f"Format Specifier .dictt = {db:.dictt}")
print(f"Format Specifier .tuplef = {db:.tuplef}") # DEPRECATED
print(f"Format Specifier .tuplet = {db:.tuplet}") # DEPRECATED
print(f"Format Specifier .key = {db:.key}")
print(f"Format Specifier .keys = {db:.keys}")
print(f"Format Specifier .values = {db:.values}")

print("Part 5 passed.")

del db

print("[green]Tests of `storage.Storage` completed sucessfully![/]")

os.remove("test_storage.json")
