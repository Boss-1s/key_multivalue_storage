#pylint: disable=line-too-long
"""
test-exceptions.py - a test file for KMS exceptions and warnings.

Compatible versions for this test file: >=kms-v1.3.0a0/2026.05.23
"""

from rich.traceback import install
from packaging.version import Version
import key_multivalue_storage as kms
from key_multivalue_storage import Storage
import warnings

install(show_locals=True)

print("Begin custom warnings/exceptions test.")

assert kms.AdditionFailureWarning
assert kms.SubtractionFailureWarning
assert kms.DeleteWarning
assert kms.CastWarning

try:
    warnings.warn(kms.AdditionFailureWarning("Test AdditionFailureWarning", __name__))
    warnings.warn(kms.SubtractionFailureWarning("Test SubtractionFailureWarning", __name__))
    warnings.warn(kms.AdditionFailureWarning(method=__name__))
    warnings.warn(kms.SubtractionFailureWarning(method=__name__))
    warnings.warn(kms.AdditionFailureWarning())
    warnings.warn(kms.SubtractionFailureWarning())
    warnings.warn(kms.DeleteWarning("Test DeleteWarning", __name__))
    warnings.warn(kms.CastWarning("Test CastWarning", __name__))
except Exception as e:
    raise AssertionError(e) from e

try:
    warnings.warn(Storage.AdditionFailureWarning("Test AdditionFailureWarning", __name__))
    warnings.warn(Storage.SubtractionFailureWarning("Test SubtractionFailureWarning", __name__))
    warnings.warn(Storage.AdditionFailureWarning(method=__name__))
    warnings.warn(Storage.SubtractionFailureWarning(method=__name__))
    warnings.warn(Storage.AdditionFailureWarning())
    warnings.warn(Storage.SubtractionFailureWarning())
    warnings.warn(Storage.DeleteWarning("Test DeleteWarning", __name__))
    warnings.warn(Storage.CastWarning("Test CastWarning", __name__))
except Exception as e:
    raise AssertionError(e) from e

try:
    raise kms.KeyNotFoundError("test.json", "random_key")
except kms.KeyNotFoundError as e:
    try:
        raise kms.KeyNotFoundError("test.json",
                                   "random_key",
                                   "This is a test for KeyNotFoundError.") from e
    except kms.KeyNotFoundError:
        pass
    except Exception as e1:
        raise AssertionError(e1) from e
except Exception as e:
    raise AssertionError(e) from e

try:
    raise kms.NoInstantiationError
except kms.NoInstantiationError:
    pass
except Exception as e:
    raise AssertionError(e) from e

if Version(kms.__version__) >= Version("1.3.0rc0"):
    try:
        @kms.kms_warnings._deprecated_arg("test_arg", "test_arg is deprecated. Please use a different argument.") #pylint: disable=line-too-long
        def test_func(test_arg=None):
            return test_arg

        test_func(test_arg="test")
    except NameError as e:
        raise AssertionError("`_deprecated_arg` does not exist. Are you using kms-semver1.3.0rc0 and later?") from e #pylint: disable=line-too-long
    except Exception as e:
        raise AssertionError(e) from e

print("Test complete.")
