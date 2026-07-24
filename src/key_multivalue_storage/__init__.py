__version__ = "v1.3.0.20260723b1.post0"
__version_internal__ = "kms-v1.3.0b1/2026.07.23a"
__author__ = "Boss_1s"
__email__ = "95505913+Boss-1s@users.noreply.github.com"
__license__ = "GPLv2"

from . import key_multivalue_storage as kms
from . import key_multivalue_storage
from .key_multivalue_storage import Storage
import warnings

warnings.warn("Going from kms-semver2.0, the module"+
              "names 'key_multivalue_storage' will be deprecated"+
              "in favor of the name 'kms'. Please note this"+
              "change accordingly, thank you!",
              PendingDeprecationWarning,
              stacklevel=4
             )

__all__ = ["Storage"]
