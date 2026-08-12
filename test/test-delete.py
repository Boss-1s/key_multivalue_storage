"""
test-delete.py - A targeted test file for delete.Delete.

Compatible versions for this test file: >=kms-v1.3.1/2026.08.12

for semver1.2.x, use the original 'test-general.py' file instead.
"""
import os
import warnings

from rich.console import Console

from key_multivalue_storage.load import Load
from key_multivalue_storage.storage import Storage
from key_multivalue_storage.delete import Delete
from key_multivalue_storage import KeyNotFoundError, DeleteWarning

print = Console().print #pylint: disable=redefined-builtin

print("Begin test for semver1.3.x Delete")

json_path = 'test-delete.json'

db_key = Storage("key", foo='bar', baz='qax')
db_key.store(json_path)

db_a1 = Storage("letters_and_numbers",
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
db_a1.store(json_path)

_names_and_address = {"Leighton Kramer":"leighton.kramer@example.com",
                      "Kylan Gentry":"kylan.gentry@example.net",
                      "Amelie Griffith":"amelia.griffith@example.org",
                      "Franklin Sierra":"f.sierra@example-mail.com",
                      "Marceline Avila":"marceline.a@example.com",
                      "Jaylen Blackwell":"jblackwell@example.net",
                      "Saoirse Conrad":"saoirse.conrad@example.org",
                      "Dilan Wolf":"dilan.wolf@example-mail.com",
                      "Jolene Fox":"jolenefox@example.com",
                      "Antonio Crosby":"antonio.crosby@example.net",
                      "Keily Meza":"k.meza@example.org",
                      "Lucian Lee":"lucian.lee@example-mail.com",
                      "Scarlett Dickson":"scarlett.d@example.com",
                      "Maxton Gill":"maxtongill@example.net",
                      "Jordan Dickerson":"jordan.d@example.org"
}

db_name_email = Storage("names_and_emails", **_names_and_address)
db_name_email.store(json_path)

del _names_and_address

print("Part 1: Delete.by_propkey()")

Delete.by_propkey(json_path, db_a1.key, 'j')
Delete.by_propkey('test-123.json', db_a1.key, 'i')
Delete.by_propkey('pyproject.toml', db_name_email.key, 'Kylan Gentry')
try:
    Delete.by_propkey(json_path, db_name_email.key, ('Kylan Gentry',)) # type: ignore
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i didn't store anything as a tuple..."
try:
    Delete.by_propkey(json_path, ('Kylan Gentry',), db_name_email.key) # type: ignore
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i didn't store anything as a tuple..."
try:
    Delete.by_propkey(json_path, 'names_an_email', 'Kylan Gentry')
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i didn't store anything as 'names_an_email'..."

loaded_db = Load.by_key(json_path, db_a1.key)

assert loaded_db is not None
assert loaded_db != db_a1
assert (db_a1 ^ loaded_db) == Storage(
    db_a1.key,
    j=10
), db_a1 ^ loaded_db

print('Part 1 passed.')
print('Part 2: Delete.by_key()')

Delete.by_key(json_path, db_a1.key)
Delete.by_key('test-123.json', db_key.key)
Delete.by_key('pyproject.toml', db_key.key)

try:
    Delete.by_key(json_path, ('Kylan Gentry',)) # type: ignore
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i didn't store anything as a tuple..."
try:
    Delete.by_key(json_path, 'names_an_email')
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Last i checked i didn't store anything under 'names_an_email'..."

try:
    loaded_db = Load.by_key(json_path, db_a1.key)
except KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Looks like Delete.by_key didn't do a good job ig"

print("Part 2 complete.")
print("Part 3: Delete.all()")

Delete.all('abc.123')
Delete.all('pyproject.toml')
Delete.all(json_path)
Delete.all(json_path, warn=False)

assert Load.by_index(json_path, 0) is None
assert Load.by_index(json_path, 1) is None

db_key.store(json_path)

assert Load.by_index(json_path, 0)

warnings.filterwarnings(category=DeleteWarning, action='ignore')

Delete.all(json_path)

assert not Load.by_index(json_path, 0)

print("Part 3 complete.")
print("[green]All tests for delete.Delete completed sucessfully![/]")

os.remove(json_path)
