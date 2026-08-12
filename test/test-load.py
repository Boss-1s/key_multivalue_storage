"""
test-load.py - A targeted test file for load.Load.

Compatible versions for this test file: >=kms-v1.3.1/2026.08.12

for semver1.2.x, use the original 'test-general.py' file instead.
"""

import ast
import os
from typing import Any

from rich.console import Console

from key_multivalue_storage.load import Load
from key_multivalue_storage.storage import Storage
from key_multivalue_storage import KeyNotFoundError

c = Console()
print = c.print

print("Begin test for semver1.3.x Load")

json_file = 'test-storage.json'
db1 = Storage("key", foo='bar', baz='qax')
db1.store('test-storage.json')
db2 = Storage("key2", foo='bar', baz='qax')
db2.store('test-storage.json')
db3 = Storage("key3", foo='bar', baz='qax')
db3.store('test-storage.json')

print("Part 1: Load.by_key()")

db4: Any = Load.by_key(json_file, 'key')

assert db4 == db1

db4 = Load.by_key('test-json.storage', 'key2')

assert db4 is None

try:
    db4 = Load.by_key(json_file, ('key3',))
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i never stored a tuple on lines 21-27..."

db4 = Load.by_key(json_file, "key3")

assert db4 == db3

print("Part 1 passed.")
print("Part 2: Load.by_index()")

db4 = Load.by_index('test.json', 0)

assert db4 is None

db4 = Load.by_index(json_file, 1)

assert db4 == db2

db4 = Load.by_index(json_file, 100000)

assert db4 is None

print("Part 2 passed.")
print("Part 3: Load.keys()")

# NOTE: Load.keys() and Storage().keys() are different methods

assert Load.keys(json_file) == ["key", "key2", "key3"]

assert Load.keys('adsjljlkads.json') is None

assert Load.keys('pyproject.toml') is None

print("Part 3 passed.")
print("Part 4: Load.values()")

db4 = Load.values(json_file, 'key', raw=False)

assert db4 == list(db1.values.values())

db4 = Load.values('test-json.storage', 'key2', raw=False)

assert db4 is None

try:
    db4 = Load.values(json_file, ('key3',))
except (KeyNotFoundError):
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i never stored a tuple on lines 21-27..."

db4 = Load.values(json_file, "key3", raw=False, keys=True)

db5 = {}

for item in db4:
    k, v = item.split(':', 1)
    item = {k.strip(): v.strip()}
    db5.update(item)

assert db5 == db3.values

print("Part 4 passed.")
print("[green]Tests for load.Load completed successfully![/]")

os.remove(json_file)
