from key_multivalue_storage import Storage

db = Storage("top_lv_key", foo="bar")

db2 = db.to_dict()
db3 = dict(db)

assert db == db2 == db3

assert isinstance(db, Storage)
assert isinstance(db2, dict)
assert isinstance(db3, dict)

assert db == {"top_lv_key": {"foo": "bar"}}
assert not db == {"top_lv_key": {"fo": "bar"}} #pylint: disable=unnecessary-negation

print(db[db.key])

