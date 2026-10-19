import warnings
from rich.markdown import Markdown
from rich.traceback import install, Traceback
from rich import print
import key_multivalue_storage as kms
from key_multivalue_storage.storage import Storage

install(show_locals=True)

print(f"NextGen is currently {kms.nextgen}")

try:
    kms.test_nextgen()
except TypeError as e:
    print(Markdown(str(e)))
except Exception as e:
    warnings.warn(f"An unexpected exception occurred: {e}")

kms.nextgen = True

kms.test_nextgen()

print(f"NextGen is now {kms.nextgen}")

print("Testing `__enter__`")

with Storage("my_key", foo="bar") as storage:
    assert isinstance(storage, Storage), f"`storage` is type {type(storage)}"
    assert storage["foo"] == "bar"
    assert dict(storage) == {"my_key": {"foo": "bar"}}

print("`__enter__` test passed.")
