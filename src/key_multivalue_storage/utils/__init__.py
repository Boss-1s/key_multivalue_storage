"""
kms Utilities.

Includes public warnings and exceptions, and private methods and metaclasses for internal use.
"""
from __future__ import annotations

__lazy_modules__ = ['morse_code_translator.translator',
                    'base64',
                    'hashlib',
                    'hmac',
                    'cryptography.hazmat.primitives.asymmetric',
                    'cryptography.hazmat.primitives.ciphers',
                    'collections.abc'
]

from collections.abc import Callable
from typing import Any, overload
import warnings as std_warnings
import base64
import hashlib
import hmac
import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing_extensions import deprecated
from public import public, private
from morse_code_translator.translator import translate_to_morse # pyright: ignore[reportMissingTypeStubs]

from . import warnings as kms_warnings, exceptions, enums

from .warnings import (
    DeleteWarning,
    AdditionFailureWarning,
    SubtractionFailureWarning,
    CastWarning,
)

from .exceptions import (
    EncodingError,
    KeyNotFoundError,
    NoInstantiationError,
    BadBitwiseOperation,
)

from .enums import Encoding, CharSet

public(
    kms_warnings=kms_warnings,
    exceptions=exceptions,
    enums=enums,
    DeleteWarning=DeleteWarning,
    AdditionFailureWarning=AdditionFailureWarning,
    SubtractionFailureWarning=SubtractionFailureWarning,
    CastWarning=CastWarning,
    KeyNotFoundError=KeyNotFoundError,
    NoInstantiationError=NoInstantiationError,
    BadBitwiseOperation=BadBitwiseOperation,
    Encoding=Encoding,
    CharSet=CharSet,
    EncodingError=EncodingError,
)

@private
@staticmethod
def _legacy_encode(string: str) -> int:
    """
    Encodes a dictionary's values using a simple character-matching system.

    ### Arguments
    - `string: dict[Any, Any]` - The dictionary to be encoded.

    ### Output
    - `dict[Any, int]` - The encoded dictionary.
    """

    std_warnings.warn(
        "The _legacy_encode function uses a simple character-matching system " \
        "which may not truly be secure.",
        EncodingWarning,
        stacklevel=13
    )

    char: str = """
    `1234657809=-\\][p';/.,lokimnjuyhbtfcvgrs edxz
    awq~+_)(*&^T$%@!#REDFGSWAQZXVCBNHYUJMKI<>LOP:{}|"?><
    """

    encoded = {}

    encoded_value: str = ""
    for char_to_encode in string:
        if char_to_encode not in char:
            raise ValueError(f"Character '{char_to_encode}' not in encoding set.")
        index = char.index(char_to_encode) + 1
        encoded_value += f"{len(str(index))}{index}"

    if encoded_value == '':
        encoded_value = f"{len(str(len(char)))}{len(char)}"

    return int(encoded_value)

_ENCODE_SHORTCUT: dict[Encoding, Callable[..., Any]] = {
    Encoding.BASE64: lambda x: base64.b64encode(x.encode()).decode(),
    Encoding.KMS: lambda x: _legacy_encode(x),
    Encoding.SHA256: lambda x: hashlib.sha256(x.encode()).hexdigest(),
    Encoding.SHA512: lambda x: hashlib.sha512(x.encode()).hexdigest(),
    Encoding.RSA: lambda x: rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    ).public_key().encrypt(
        x.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashlib.sha256()),
            algorithm=hashlib.sha256(),
            label=None
        )
    ),
    Encoding.HMAC: lambda x, y: hmac.new(y, x.encode(), hashlib.sha256).hexdigest(),
    Encoding.AES: lambda x, y: (
        lambda iv: base64.b64encode(
            iv + Cipher(
                algorithms.AES(y),
                modes.CBC(iv)
            ).encryptor().update(
                sym_padding.PKCS7(128).padder().update(x.encode()) +
                sym_padding.PKCS7(128).padder().finalize()
            )
        ).decode()
    )(os.urandom(16)),
    Encoding.MORSE: lambda x: translate_to_morse(x),#FIXME:Morse does not support non-alphanumeric
    Encoding.HEX: lambda x, y: x.encode(y).hex(),
    Encoding.NONE: lambda x: x,
}

def _encode_item(item,
                 *,
                 encoding: Encoding | str,
                 secondary_arg: Any = None) -> bytes | str:
    """
    Helper function to look up and apply a specific encoding strategy.

    This is part of the completely overhauled version of the original encoding
    system. To preserve backwards compatibility within this update (`kms-semver1.4.0`),
    defaults have been set to `Encoding.KMS` (the original legacy character mapping system)
    and `utf-8` for the default encoding and default character set, respectively.

    ## Arguments
    - `item: Any`: The item to encode.

    ## Keyword Arguments
    - `encoding: Encoding | str`: The encoding strategy to use.
    - `secondary_arg: Any`: An optional secondary argument for certain encoding strategies. \
    See more below.

    ## Output
    - `bytes | str`: The encoded item.

    ## The Secondary Argument

    The `secondary_arg` is used for encoding strategies that require an additional parameter.
    For example, HMAC and AES encoding strategies use this argument to pass the key.
    The following is a list of each encoding strategy and its corresponding use of the
    `secondary_arg`:
    - `Encoding.HMAC`: Uses `secondary_arg` as the key for HMAC.
    - `Encoding.AES`: Uses `secondary_arg` as the key for AES encryption.
    - `Encoding.HEX`: Uses `secondary_arg` as the character set for encoding to hex.
    """
    if isinstance(encoding, str):
        encoding = Encoding(encoding.lower())
    encoder = _ENCODE_SHORTCUT.get(encoding, _ENCODE_SHORTCUT[Encoding.KMS])
    if encoding in [Encoding.HMAC, Encoding.AES, Encoding.HEX]:
        if secondary_arg is None:
            raise EncodingError(f"Encoding strategy {encoding} requires a secondary argument")
        return encoder(str(item), secondary_arg)
    return encoder(str(item))

def _encode(data: Any,
            *,
            encoding: Encoding | str = Encoding.KMS,
            charset: CharSet | str = CharSet.UTF8,
            encode_keys: bool = False,
            secondary_arg: Any = None) -> Any:
    """
    Encodes keys and values in dicts, lists, or primitive types recursively.

    This is part of the completely overhauled version of the original encoding
    system. To preserve backwards compatibility within this update (`kms-semver1.4.0`),
    defaults have been set to `Encoding.KMS` (the original legacy character mapping system)
    and `utf-8` for the default encoding and default character set, respectively.

    ## Arguments
    - `data: Any`: The data to encode.

    ## Keyword Arguments
    - `encoding: Encoding | str`: The encoding strategy to use.
    - `charset: CharSet | str`: The character set to use.
    - `secondary_arg: Any`: An optional secondary argument for certain encoding strategies. \
    See more below.

    ## Output
    - `Any`: The encoded data. Probably either bytes or string *values*
    depending on the encoding strategy.

    ## The Secondary Argument

    The `secondary_arg` is used for encoding strategies that require an additional parameter.
    For example, HMAC and AES encoding strategies use this argument to pass the key.
    HEX encoding uses this argument to specify the character set for encoding to hex.
    The following is a list of each encoding strategy and its corresponding use of the
    `secondary_arg`:

    - `Encoding.HMAC`: Uses `secondary_arg` as the key for HMAC.
    - `Encoding.AES`: Uses `secondary_arg` as the key for AES encryption.
    - `Encoding.HEX`: Uses `secondary_arg` as the character set for encoding to hex.
    """
    if isinstance(data, dict):
        if encode_keys:
            return {
                _encode_item(k,
                             encoding=encoding,
                             secondary_arg=secondary_arg
                ): _encode(v,
                           encoding=encoding,
                           charset=charset,
                            encode_keys=encode_keys,
                            secondary_arg=secondary_arg)
                for k, v in data.items()
            }
        return {
            k: _encode(v,
                       encoding=encoding,
                       charset=charset,
                       encode_keys=encode_keys,
                       secondary_arg=secondary_arg)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [_encode(item,
                       encoding=encoding,
                       charset=charset,
                       secondary_arg=secondary_arg
                       ) for item in data]

    return _encode_item(data, encoding=encoding, secondary_arg=secondary_arg)

@private
@staticmethod
def _decode(to_decode: dict[Any, Any]) -> dict[Any, Any]:
    """
    Decodes a dict encoded with `kms.utils._encode`.

    ### Arguments
    - `to_decode: dict[Any, Any]`: The encoded object.

    ### Output
    - `dict[Any, Any]`: The decoded object.
    """

    if not isinstance(to_decode, dict):
        raise TypeError("Expected encoded dictionary for decoding.")

    char: str = """
    `1234657809=-\\][p';/.,lokimnjuyhbtfcvgrs edx
    zawq~+_)(*&^T$%@!#REDFGSWAQZXVCBNHYUJMKI<>LOP:{}|"?><
    """

    decoded = {}

    for k, v in to_decode.items():
        if not isinstance(k, str):
            k = str(k)

        if not isinstance(v, int):
            try:
                v = int(v)
            except Exception as e:
                raise TypeError(f"Expected int for decoding, got {type(v)}.") from e

        v_str: str = str(v)
        decoded_value: str = ""
        i: int = 0

        while i < len(v_str):
            length_of_index: int = int(v_str[i])
            index: int = int(v_str[i + 1:i + 1 + length_of_index]) - 1
            decoded_value += char[index]
            i += 1 + length_of_index

        decoded[k] = decoded_value

    return decoded
