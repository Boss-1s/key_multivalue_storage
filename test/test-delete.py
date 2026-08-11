"""
test-delete.py - A targeted test file for delete.Delete.

Compatible versions for this test file: >=kms-v1.3.1/2026.08.12

for semver1.2.x, use the original 'test-general.py' file instead.
"""
from rich.console import Console

from key_multivalue_storage.load import Load
from key_multivalue_storage.storage import Storage
from key_multivalue_storage.delete import Delete
from key_multivalue_storage import KeyNotFoundError

print = Console().print

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

loaded_db = Load.by_key(json_path, db_a1.key)

assert loaded_db is not None
assert loaded_db != db_a1
assert (db_a1 ^ loaded_db) == Storage(
    db_a1.key,
    j=10
), db_a1 ^ loaded_db
