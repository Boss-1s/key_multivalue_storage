""""Meta classes for modules"""

from __future__ import annotations

class _StorageMeta(type):
    """
    Metadata variables for Storage module
    """
    @property
    def semver(cls) -> str:
        """Current semnatic version of this module."""
        return "v1.3.0a0"

    @property
    def calver(cls) -> str:
        """Current calendar version of this module."""
        return "2026.05.22"

    @property
    def version(cls) -> str:
        """Current full version of this module."""
        return "kms-"+cls.semver+"/"+cls.calver

    @property
    def last_update(cls) -> str:
        """Date this module was last updated."""
        return "2026/5/22"
