__version__ = "v1.1.1.20251205"
__version_internal__ = "kms-v1.1.1/2025.12.05"
__author__ = "Boss_1s"
__email__ = "95505913+Boss-1s@users.noreply.github.com"
__license__ = "GPLv2"

from . import key_multivalue_storage as kms
from . import key_multivalue_storage
from .key_multivalue_storage import Storage

__all__ = ["Storage"]
