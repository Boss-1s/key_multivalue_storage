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

# Ensure Division still works properly after refactorization #

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
