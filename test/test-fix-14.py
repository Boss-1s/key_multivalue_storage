# type: ignore
# pylint: disable=redefined-builtin, missing-module-docstring, missing-method-docstring, global-variable-undefined
import sys, io, builtins
from warnings import warn

try:
    from rich.console import Console
    RICH = True
except ImportError:
    RICH = False
    warn('Rich is not installed.')

import key_multivalue_storage as kms

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
        print(f"Part {int(boolean) + 1}.1: UTF-8 test")
        change_stream_encoding('utf-8', no_color=boolean)

        kms.help()

        reset()
        print(f"Part {int(boolean) + 1}.1 passed.")

        # --- Part 2: ASCII ---
        print(f"Part {int(boolean) + 1}.2: ASCII test")
        change_stream_encoding('ascii', no_color=boolean)

        kms.help()

        reset()
        print(f"Part {int(boolean) + 1}.2 passed.")

        # --- Part 3: CP1252 ---
        print(f"Part {int(boolean) + 1}.3: CP1252 test")
        change_stream_encoding('cp1252', no_color=boolean)

        kms.help()

        reset()
        print(f"Part {int(boolean) + 1}.3 passed.")

        # --- Part 4: CP437 ---
        print(f"Part {int(boolean) + 1}.4: CP437 test")
        change_stream_encoding('CP437', no_color=boolean)

        kms.help()

        reset()
        print(f"Part {int(boolean) + 1}.4 passed.")

        # --- Part 5: latin-1 ---
        print(f"Part {int(boolean) + 1}.5: latin-1 test")
        change_stream_encoding('latin-1', no_color=boolean)

        kms.help()

        reset()
        print(f"Part {int(boolean) + 1}.5 passed.")

    # --- Part 3: Raw Bytes (No Encoding) ---
    print("Part 3: Raw Bytes / No Encoding test")
    change_stream_to_raw_bytes()

    kms.help()

    reset()
    print("Part 3 passed.")

    print("Test complete, all parts passed.")

    sys.exit(0)
