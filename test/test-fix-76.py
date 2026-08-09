from key_multivalue_storage import Storage

db1 = Storage("key", foo="bar")

db2 = Storage("key", baz="qax")

db3 = db1 + db2

assert db3 == Storage("key", foo="bar", baz="qax")
assert db1 == Storage("key", foo="bar")
assert db2 == Storage("key", baz="qax")


db4 = db1 + {'a': 'b'}

assert db4 == Storage("key", foo="bar", a="b")
assert db1 == Storage("key", foo="bar")

db5 = db1 + ['a', 'b']

assert db5 == Storage("key", foo="bar", undefined=['a', 'b'])
assert db1 == Storage("key", foo="bar")
