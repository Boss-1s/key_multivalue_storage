__version__ = "v1.2.0.20260128.1"
__version_internal__ = "kms-v1.2/2026.01.28a"
__author__ = "Boss_1s"
__email__ = "95505913+Boss-1s@users.noreply.github.com"
__license__ = "GPLv2"

from . import key_multivalue_storage as kms
from . import key_multivalue_storage
from .key_multivalue_storage import Storage

__all__ = ["Storage"]
