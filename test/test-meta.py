# type: ignore
# pylint: disable=redefined-builtin, missing-module-docstring, missing-method-docstring, global-variable-undefined
"""
test-meta.py - a test file for KMS designed specifaclly to test the new metaclass
and help() method implementations.

Compatible versions for this test file: >=kms-v1.3.0/2026.07.30
"""

from __future__ import annotations

import sys
import builtins
from rich.console import Console

import key_multivalue_storage as kms
from key_multivalue_storage import (
    storage,
    load,
    edit,
    delete
)
from key_multivalue_storage.storage import Storage
from key_multivalue_storage.load import Load
from key_multivalue_storage.edit import Edit
from key_multivalue_storage.delete import Delete
from key_multivalue_storage.utils.metadata import _KmsMeta

print = builtins.print

print("Begin test\n"+("-"*20)+"\nPart 1: __str__ and __repr__ of class via metaclass\n"+("-"*20))

try:
    print(Storage)
    print(Storage.Load)
    print(Storage.Edit)
    print(Storage.Delete)
except Exception as e:
    raise AssertionError from e

try:
    print(repr(Storage))
    print(repr(Storage.Load))
    print(repr(Storage.Edit))
    print(repr(Storage.Delete))
except Exception as e:
    raise AssertionError from e

assert str(Storage) == repr(Storage)
assert str(Storage.Load) == repr(Storage.Load)
assert str(Storage.Edit) == repr(Storage.Edit)
assert str(Storage.Delete) == repr(Storage.Delete)

print("Part 1 passed.")
print("-"*20)
print("Part 2: help() method for each class")

try:
    kms.help() # Module Help

    storage.help() # storage Module Help
    Storage.help()
    Storage.help(Storage.store)

    load.help()
    Storage.Load.help()
    Storage.Load.help(Storage.Load.keys)

    edit.help()
    Storage.Edit.help()
    Storage.Edit.help(Storage.Edit.propkey)

    delete.help()
    Storage.Delete.help()
    Storage.Delete.help(Storage.Delete.all)

except Exception as e:
    console = Console()
    console.print_exception(show_locals=True)
    console.print(f"[b red]Error: {e}")
    sys.exit(1)

print("Part 2 passed.")
print("-"*20)
print("Part 3: Ensure _KmsMeta can fail correctly")

try:
    class BadMetaClass(metaclass=_KmsMeta): # pylint: disable=unused-variable, too-few-public-methods, line-too-long
        pass
except TypeError as e:
    print(f"Expected TypeError caught: {e}")
except Exception as e:
    raise AssertionError(e) from e

print("Part 3 passed.")
print("-"*20)
print("Part 4: Ensure version properties work")

assert kms.__version__
assert kms.__version_internal__
# -Storage- #
assert Storage.semver
assert Storage.calver
assert Storage.version
assert Storage.last_update
# -DEPRECATED- #
assert Storage.VERSION
assert Storage.LAST_UPDATE
assert Storage.DATE_VERSION
# -Load- #
assert Load.semver
assert Load.calver
assert Load.version
assert Load.last_update
# -Edit- #
assert Edit.semver
assert Edit.calver
assert Edit.version
assert Edit.last_update
# -Delete- #
assert Delete.semver
assert Delete.calver
assert Delete.version
assert Delete.last_update

print("Part 4 passed.")
print("Part 5: Ensure help() method works for all encodings")

import io
from warnings import warn

try:
    from rich.console import Console
    RICH = True
except ImportError:
    RICH = False
    warn('Rich is not installed.')


# Global context tracking for our dynamic prints
current_stream = None
console = None

def change_stream_encoding(encoding_name: str, *, no_color: bool = False):
    """Safely builds a brand new isolated stream using the raw standard output descriptor."""
    global current_stream, console, print

    sys.stdout.flush()

    if current_stream and current_stream is not sys.__stdout__:
        try:
            current_stream.flush()
        except Exception:
            pass

    current_stream = io.TextIOWrapper(
        open(1, mode='wb', closefd=False),
        encoding=encoding_name,
        line_buffering=True
    )

    sys.stdout = current_stream

    if RICH:
        if no_color:
            # INFO: color_system=None strips ANSI codes.
            # INFO: force_terminal=True ensures Rich doesn't auto-detect
            console = Console(file=current_stream, color_system=None, force_terminal=True)
        else:
            console = Console(file=current_stream, force_terminal=True)
        print = console.print
    else:
        print = builtins.print

def change_stream_to_raw_bytes():
    """Bypasses all encoding layers by pointing stdout directly to the raw binary buffer."""
    global current_stream, console, print

    sys.stdout.flush()

    # Target the raw, unencoded binary writer of standard output
    current_stream = sys.__stdout__.buffer
    sys.stdout = current_stream  # Warning: normal print() will crash here!

    if RICH:
        # Rich knows how to write directly to a raw byte stream if we force it
        console = Console(file=current_stream, force_terminal=True)
        print = console.print
    else:
        # Pure Python print() expects strings. We must override it to accept and write raw bytes.
        def raw_byte_print(*arg, sep=b' ', end=b'\n'):
            # Convert args to bytes if they are strings, or use raw bytes
            byte_args = [
                a if isinstance(a, bytes) else str(a).encode('utf-8', errors='ignore') for a in arg
            ]
            current_stream.write(sep.join(byte_args) + end)
            current_stream.flush()
        print = raw_byte_print

def reset():
    """Points stdout right back to the native environment defaults."""
    global console, print
    sys.stdout = sys.__stdout__
    if RICH:
        console = Console(file=sys.__stdout__)
        print = console.print
    else:
        print = builtins.print

reset()

print("Begin patch test for issue #14.")

# try:
if isinstance(sys.__stdout__, io.TextIOWrapper):
    print("[green bold]Using TextIOWrapper tracking path[/]")

    for boolean in [False, True]:
        print(f"[b]no_color[/] will be set to [green italic]{boolean}[/]")
        # --- Part 1: UTF-8 ---
        print(f"Part 5.{int(boolean) + 1}.1: UTF-8 test")
        change_stream_encoding('utf-8', no_color=boolean)

        kms.help()

        reset()
        print(f"Part 5.{int(boolean) + 1}.1 passed.")

        # --- Part 2: ASCII ---
        print(f"Part 5.{int(boolean) + 1}.2: ASCII test")
        change_stream_encoding('ascii', no_color=boolean)

        kms.help()

        reset()
        print(f"Part 5.{int(boolean) + 1}.2 passed.")

        # --- Part 3: CP1252 ---
        print(f"Part 5.{int(boolean) + 1}.3: CP1252 test")
        change_stream_encoding('cp1252', no_color=boolean)

        kms.help()

        reset()
        print(f"Part 5.{int(boolean) + 1}.3 passed.")

        # --- Part 4: CP437 ---
        print(f"Part 5.{int(boolean) + 1}.4: CP437 test")
        change_stream_encoding('CP437', no_color=boolean)

        kms.help()

        reset()
        print(f"Part 5.{int(boolean) + 1}.4 passed.")

        # --- Part 5: latin-1 ---
        print(f"Part 5.{int(boolean) + 1}.5: latin-1 test")
        change_stream_encoding('latin-1', no_color=boolean)

        kms.help()

        reset()
        print(f"Part 5.{int(boolean) + 1}.5 passed.")

    # --- Part 5.3: Raw Bytes (No Encoding) ---
    print("Part 5.3: Raw Bytes / No Encoding test")
    change_stream_to_raw_bytes()

    kms.help()

    reset()
    print("Part 5.3 passed.")

    print("Test complete, all parts passed.")

print("Part 5 passed.")

print("Test file completed successfully.")
