"initiation"

__version__ = "1.2.2.20260517.2"
__version_internal__ = "kms-v1.2.2/2026.05.17b"
__author__ = "Boss_1s"
__email__ = "95505913+Boss-1s@users.noreply.github.com"
__license__ = "GPLv2"

import warnings

from . import key_multivalue_storage as kms
from . import key_multivalue_storage
from .key_multivalue_storage import Storage

__all__ = ["Storage"]

warnings.warn("Going from kms-semver2.0, the module"+
              "names 'key_multivalue_storage' will be deprecated"+
              "in favor of the name 'kms'. Please note this"+
              "change accordingly, thank you!",
              PendingDeprecationWarning,
              stacklevel=4
             )

warnings.warn("kms-v1.x will be officially discontinued soon."+
              "The last major content update will be kms-v1.6, most "+
              "likely around the time kms-v2.1 comes out. Please "+
              "stay tuned to avoid version compatibility conflicts.",
              PendingDeprecationWarning
             )
