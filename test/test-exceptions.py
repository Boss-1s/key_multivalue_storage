#pylint: disable=line-too-long
"""
test-exceptions.py - a test file for KMS exceptions and warnings.

Compatible versions for this test file: >=kms-v1.3.0a0/2026.05.23
"""

from rich.traceback import install
import key_multivalue_storage as kms

install(show_locals=True)

print("Begin custom warnings/exceptions test.")

assert kms.AdditionFailureWarning
assert kms.SubtractionFailureWarning
assert kms.DeleteWarning
assert kms.CastWarning

try:
    raise kms.KeyNotFoundError("Test KeyNotFoundError", "This is a test for KeyNotFoundError.")
except kms.KeyNotFoundError:
    pass
except Exception as e:
    raise AssertionError(e) from e

try:
    raise kms.NoInstantiationError
except kms.NoInstantiationError:
    pass
except Exception as e:
    raise AssertionError(e) from e

print("Test complete.")
