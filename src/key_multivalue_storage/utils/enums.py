"""
kms enumerations.

Enums are for Pythonic purposes only, escpecially in a case where one specific logic has many
different values that can be passed, and these values also affect the library as a whole.
"""
from __future__ import annotations
from typing import Literal

__lazy_modules__ = ["sys"]

from enum import Enum
import sys

warnings = sys.modules.get("warnings")

class Encoding(Enum):
    """
    Enum class for encoding types, new in kms-semver1.4.0.
    """
    UTF8 = "utf-8"
    UTF16 = "utf-16"
    UTF32 = "utf-32"
    ASCII = "ascii"
    BASE64 = "base64"
    KMS = "kms_default"
    SHA256 = "sha256"
    SHA512 = "sha512"
    SHA1 = "sha1"
    RSA = "rsa"
    AES = "aes"
    HMAC = "hmac"
    PIGPEN = "pigpen"
    MORSE = "morse_code"
    NONE = None

    @classmethod
    def _missing_(cls, value):
        """
        Handle missing values by returning the DEFAULT encoding.
        """
        warnings.warn(f"{value} is not a valid Encoding; defaulting to '{cls.KMS}'",#type: ignore
                      UserWarning)
        return cls.KMS
