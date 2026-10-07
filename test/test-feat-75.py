from __future__ import annotations

from key_multivalue_storage.storage import Storage

# __iadd__ #

db = Storage("test", a=1, b=2, c=3)
db2 = Storage("test", d=4, e=5, f=6)
db3 = {"g": 7, "h": 8, "i": 9}
db4 = [10, 11, 12]
db5 = {"a": {"nested": "value"}, "b": 2}

db += db2

assert db.values == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6}
assert isinstance(db, Storage)
assert db2.values == {"d": 4, "e": 5, "f": 6}

db += db3

assert db.values == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9}
assert isinstance(db, Storage)
assert db3 == {"g": 7, "h": 8, "i": 9}

db += db4

assert db.values == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9,
                     "undefined": [10, 11, 12]}
assert isinstance(db, Storage)
assert db4 == [10, 11, 12]

db += db5 # Nested test (should raise warning)

assert db.values == {"a": {"nested": "value"}, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9,
                     "undefined": [10, 11, 12]}
assert isinstance(db, Storage)
assert db5 == {"a": {"nested": "value"}, "b": 2}