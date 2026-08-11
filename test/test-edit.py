"""
test-edit.py - A targeted test file for edit.Edit.

Compatible versions for this test file: >=kms-v1.3.1/2026.08.12

for semver1.2.x, use the original 'test-general.py' file instead.
"""

import os

from rich.console import Console

from key_multivalue_storage.load import Load
from key_multivalue_storage.storage import Storage
from key_multivalue_storage.edit import Edit

print = Console().print

print("Begin test for edit.Edit")

json_path = 'test-edit.json'

db_key = Storage("key", foo='bar', baz='qax')
db_key.store('test-edit.json')

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
db_a1.store('test-edit.json')

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

print("Part 1: Edit.propkey() / Edit.propval()")

Edit.propkey(
    json_path,
    "letters_and_numbers",
    "k",
    "k",
    new=True
)

Edit.propval(
    json_path,
    "letters_and_numbers",
    "k",
    "11"
)

loaded_db = Load.by_key(json_path, "letters_and_numbers")

assert loaded_db is not None
assert loaded_db != db_a1
assert (loaded_db ^ db_a1) == Storage("letters_and_numbers", k='11')

Edit.propkey(
    json_path,
    "names_and_emails",
    "Scarlett Dickson",
    "Skylar Dickerson"
)

Edit.propval(
    json_path,
    "names_and_emails",
    "Skylar Dickerson",
    "skylar.d@example.com"
)

loaded_db = Load.by_key(json_path, "names_and_emails")

assert loaded_db is not None
assert loaded_db != db_name_email
assert (loaded_db ^ db_name_email) == Storage(
    "names_and_emails",**{
        "Skylar Dickerson": "skylar.d@example.com",
        "Scarlett Dickson": "scarlett.d@example.com"
    }
), (loaded_db ^ db_name_email)

print("Part 1 complete.")

os.remove('test-edit.json')
