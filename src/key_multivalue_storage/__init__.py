__version__ = "v1.2.3.20260605.4b3"
__version_internal__ = "kms-v1.2.3b3/2026.06.05d"
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
