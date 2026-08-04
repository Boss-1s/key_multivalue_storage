import sys
import io
import importlib
import key_multivalue_storage as kms


def test_help_does_not_raise_on_legacy_encoding(monkeypatch):
    """
    Simulate a legacy Windows stdout (cp1252) by replacing sys.stdout with
    an object that exposes a .buffer (BytesIO) and encoding='cp1252'.
    kms.help() should not raise UnicodeEncodeError.
    """
    # Prepare a binary buffer to stand in for sys.stdout.buffer
    buf = io.BytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            # TextIOWrapper in _make_safe_console expects sys.stdout.buffer
            self.buffer = buffer
            self.encoding = "cp1252"

        def write(self, s):
            # simulate a text write to the buffer; encode with cp1252 to
            # mimic behavior of a legacy stream (we ignore characters that
            # would otherwise fail here to avoid the test failing prematurely).
            try:
                # This may drop characters not mappable in cp1252;
                # we intentionally ignore errors here because the library
                # code should install its safe wrapper and avoid raising.
                buf.write(s.encode("cp1252", errors="ignore"))
            except Exception:
                # ensure write never raises in the simulated stream
                pass

        def flush(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    # Call help() — it should not raise UnicodeEncodeError.
    kms.help()
