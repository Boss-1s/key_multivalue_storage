__version__ = "v1.0.0.20250817"
__version_internal__ = "kms-v1.0.0/2025.08.17"
__author__ = "Boss_1s"
__email__ = "95505913+Boss-1s@users.noreply.github.com"
__license__ = "GPLv2"

from . import key_multivalue_storage as kms
from . import key_multivalue_storage
from .key_multivalue_storage import Storage

__all__ = ["Storage"]
