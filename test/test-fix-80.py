from key_multivalue_storage import Storage

# Simple Subtraction #

db1 = Storage("key", foo="bar", baz="qax")
db2 = Storage("key", foo="bar")
db3 = Storage("key", baz="qax")

db4 = db1 - db2

assert db3 == db4
assert db1 == Storage("key", foo="bar", baz="qax")

# Complex Subtraction #

db1 = Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")
db2 = dict(Storage("key", foo="bar", baz="qax", c="d", g="h", i="j").values)
db3 = Storage("key", a='b', e='f')

db4 = db1 - db2

assert db3 == db4
assert db1 == Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")

# Reverse Subtraction #

db2 = dict(Storage("key", foo="bar", baz="qax", c="d", g="h", i="j").values)

db4 = db2 - db1

assert db3 == db4
assert db1 == Storage("key", foo="bar", baz="qax", a="b", c="d", e="f", g="h")
