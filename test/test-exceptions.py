import key_multivalue_storage as kms
from rich.traceback import install

install(show_locals=True)

print("Begin custom warnings/exceptions test.")

assert kms.AdditionFailureWarning
assert kms.SubtractionFailureWarning
assert kms.DeleteWarning
assert kms.CastWarning

try:
  raise kms.KeyNotFoundError
except kms.KeyNotFoundError:
  pass
except Exception as e:
  raise AssertionError(e)
else:
  raise AssertionError

try:
  raise kms.NoInstantiationError
except kms.NoInstantiationError:
  pass
except Exception as e:
  raise AssertionError(e)
else:
  raise AssertionError

print("Test complete.")
