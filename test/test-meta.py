"""
test-meta.py - a test file for KMS designed specifaclly to test the new metaclass 
and help() method implementations.

Test file version: t-meta-kms-v2026.7.1
Compatible versions for this test file: >=kms-v1.3.0a/2026.07.03
"""

import key_multivalue_storage as kms
from key_multivalue_storage import Storage

VERSION = "t-meta-kms-v2026.7.1"

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
    kms.kms.help() # storage Module Help
    Storage.help() # Storage *class* Help
    Storage.help(Storage.store)
    Storage.Load.help()
    Storage.Load.help(Storage.Load.keys)
    # Storage.Edit.help()
    # Storage.Edit.help(Storage.Edit.propkey)
    # Storage.Delete.help()
    # Storage.Delete.help(Storage.Delete.all)
except Exception as e:
    raise AssertionError from e

print("Part 2 passed.")
print("Test file completed successfully.")
