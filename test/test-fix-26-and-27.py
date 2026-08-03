# pylint: skip-file
from key_multivalue_storage import Storage
from typing import Any

db: Storage = Storage("my_key", foo="bar", baz="qux")

db2: dict[str, dict[str, Any]] = db

print(type(db))
print(type(db2))
