# NOTE: this is actually ripped straight from test-storage.py

from key_multivalue_storage import Storage
from rich.console import Console

db1 = Storage("key", foo='bar', baz='qax')
db3 = Storage("key", qwert='yuiop')

try:
    db1 | Storage("whoops_wrong_key", foo='bar')
except ValueError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "Storage objects with different keys should not be operable..."

db4 = db1 | db3

assert isinstance(db4, Storage)
assert db4.values == {'foo': 'bar',
                      'baz': 'qax',
                      'qwert':'yuiop'
}

Console().print(db1)

db4 = db1 | dict(db3.values)
Console().print(db4)
assert isinstance(db4, Storage)
assert db4.values == {'foo': 'bar', # <<<--- HERE
                      'baz': 'qax',
                      'qwert':'yuiop'
}

try:
    1000.625 | db1 #type: ignore
except TypeError:
    pass
except Exception as e:
    raise AssertionError(e) from e
else:
    assert False, "float and Stoarge cannot be operated on with bitwise operator OR"
