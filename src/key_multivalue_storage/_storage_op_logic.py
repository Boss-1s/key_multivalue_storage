# pylint: skip-file

"""
Maybe, maybe not. we'll see. optimizations will definitely be needed,
just not right now.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self, TypeVar
import warnings

from .utils.warnings import AdditionFailureWarning, SubtractionFailureWarning

if TYPE_CHECKING:
    from .storage import Storage

def add(x, y, *, inplace: bool = False):
    _temp_values: dict[Any, Any] = {}

    if isinstance(y, type(x)):
        if x.key != y.key:
            raise ValueError(x._default_valueerror_msg)
        _temp_values = y.values

    if isinstance(y, dict):
        if any(isinstance(value, dict) for value in y.values()):
            warnings.warn("Passing a nested dictionary may break the addition process.",
                            RuntimeWarning)
        warnings.warn(AdditionFailureWarning(method="__add__"))
        _temp_values = y

    if isinstance(y, list):
        warnings.warn(AdditionFailureWarning(method="__add__"))
        _temp_values = {"undefined": y}

    if inplace:
        x.values.update(_temp_values)
        return x
    _temp_dict = dict(x.values)
    _temp_dict.update(_temp_values)

    return _temp_dict

def sub(x, y, *, inplace: bool = False):
    _skeys = set()
    _other_dict = {}

    if isinstance(y, type(x)):
        if x.key != y.key:
            raise ValueError(x._default_valueerror_msg)
        _skeys: set[str] = set(x.values.keys()) & set(y.values.keys())
        _other_dict = y.values

    elif isinstance(y, dict):
        warnings.warn(SubtractionFailureWarning(method="__sub__"))
        _skeys: set[str] = set(x.values.keys()) & set(y)
        _other_dict = y

    _temp_dict = dict(x.values)

    for akey in _skeys:
        if akey in _temp_dict:
            del _temp_dict[akey]
        else:
            _temp_dict[akey] = _other_dict[akey]

    if inplace:
        x.values = _temp_dict
        return x
    return _temp_dict

def true_div(x, y, *, inplace: bool = False):
    if y > 9:
        # TODO in v2.0: decimal.DivisionImpossible
        raise ValueError("Dividing by a number greater than nine is unsupported")

    split: float | int = len(x.values.keys()) / y

    if len(x.values.keys()) == split:
        return [create_storage(x.key, **x.values)]

    if not split.is_integer():
        # TODO in v2.0: decimal.DivisionImpossible
        raise ValueError(f"Cannot divide by number {y} for a "+
                        f"list length of {len(x.values.keys())}")

    _temp_dict: dict[str, Any] = {}
    _my_keys = list(x.values.keys())
    split = int(split)
    returnlist: list[Storage] = []

    for i in range(y):
        for j in range(split):
            _current_key = _my_keys[(j + (i * split))]
            _temp_dict.update({_current_key: x.values[_current_key]})
        returnlist.append(Storage(x.key, **_temp_dict))
        _temp_dict = {}

    return returnlist
