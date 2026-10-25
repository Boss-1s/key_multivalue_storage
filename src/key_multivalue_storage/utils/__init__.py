"""
kms Utilities.

Includes public warnings and exceptions, and private methods and metaclasses for internal use.
"""

from typing import Any, overload

from typing_extensions import deprecated
from public import public, private

from . import warnings as kms_warnings, exceptions

from .warnings import (
    DeleteWarning,
    AdditionFailureWarning,
    SubtractionFailureWarning,
    CastWarning,
)

from .exceptions import (
    KeyNotFoundError,
    NoInstantiationError,
    BadBitwiseOperation
)

public(
    kms_warnings=kms_warnings,
    exceptions=exceptions,
    DeleteWarning=DeleteWarning,
    AdditionFailureWarning=AdditionFailureWarning,
    SubtractionFailureWarning=SubtractionFailureWarning,
    CastWarning=CastWarning,
    KeyNotFoundError=KeyNotFoundError,
    NoInstantiationError=NoInstantiationError,
    BadBitwiseOperation=BadBitwiseOperation,
)

@private
@staticmethod
def _encode(to_encode: dict[Any, Any]) -> dict[Any, int]:
    """
    Encodes a dictionary's values using a simple character-matching system.

    ### Arguments
    - `string: dict[Any, Any]` - The dictionary to be encoded.

    ### Output
    - `dict[Any, int]` - The encoded dictionary.
    """

    char: str = """
    `1234657809=-\\][p';/.,lokimnjuyhbtfcvgrs edxz
    awq~+_)(*&^T$%@!#REDFGSWAQZXVCBNHYUJMKI<>LOP:{}|"?><
    """

    encoded = {}

    for k, v in to_encode.items():
        if not isinstance(k, str):
            k = str(k)

        if not isinstance(v, str):
            try:
                v = str(v)
            except Exception as e:
                raise TypeError(f"Expected string for encoding, got {type(v)}.") from e

        encoded_value: str = ""
        for char_to_encode in v:
            if char_to_encode not in char:
                raise ValueError(f"Character '{char_to_encode}' not in encoding set.")
            index = char.index(char_to_encode) + 1
            encoded_value += f"{len(str(index))}{index}"

        if encoded_value == '':
            encoded_value = f"{len(str(len(char)))}{len(char)}"

        encoded[k] = int(encoded_value)

    return encoded

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
