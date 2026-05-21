__version__ = "1.2.2.20260517.2"
__version_internal__ = "kms-v1.2.2/2026.05.17b"
__author__ = "Boss_1s"
__email__ = "95505913+Boss-1s@users.noreply.github.com"
__license__ = "GPLv2"

from . import key_multivalue_storage as kms
from . import key_multivalue_storage
from . import key_multivalue_storage as key-multivalue-storage
from .key_multivalue_storage import Storage
import warnings

warnings.warn("Going from kms-semver2.0, the module"+
              "names 'key_multivalue_storage' and"+
              "'key-multivalue-storage' will be deprecated"+
              "in favor of the name 'kms'. Please note this"+
              "change accordingly, thank you!",
              PendingDeprecationWarning
             )

__all__ = ["Storage"]
