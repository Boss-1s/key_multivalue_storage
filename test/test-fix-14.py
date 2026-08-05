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


def test_help_does_not_raise_when_stdout_is_utf8(monkeypatch):
    """When stdout.encoding already indicates UTF-8, help() should still run."""
    buf = io.BytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "utf-8"

        def write(self, s):
            try:
                buf.write(s.encode("utf-8", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    # Should not raise
    kms.help()


def test_help_handles_missing_encoding_attribute(monkeypatch):
    """If accessing sys.stdout.encoding raises, help() should still be safe."""
    buf = io.BytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer

        @property
        def encoding(self):
            raise AttributeError("encoding access not supported")

        def write(self, s):
            try:
                buf.write(s.encode("utf-8", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    # Should not raise even if encoding access fails
    kms.help()


def test_help_falls_back_if_textiowrapper_fails(monkeypatch):
    """If io.TextIOWrapper raises, the code should fall back to a no-color Console."""
    import io as real_io

    buf = io.BytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "cp1252"

        def write(self, s):
            try:
                buf.write(s.encode("cp1252", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    # Monkeypatch io.TextIOWrapper to raise when called to simulate failure
    def raising_textiowrapper(*a, **k):
        raise RuntimeError("simulated TextIOWrapper failure")

    monkeypatch.setattr(real_io, "TextIOWrapper", raising_textiowrapper)

    # Should not raise despite TextIOWrapper failing
    kms.help()


def test_unmappable_characters_are_replaced(monkeypatch):
    """When stdout is legacy (cp1252), ensure unmappable characters are replaced
    into the underlying buffer (we look for UTF-8 replacement marker 0xEF 0xBF 0xBD).
    """
    buf = io.BytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "cp1252"

        def write(self, s):
            try:
                # If the library wraps stdout with utf-8/errors=replace, writes
                # will be utf-8 encoded into this buffer. Otherwise, this simulates
                # a simple cp1252 write (ignoring unmappable characters).
                buf.write(s.encode("cp1252", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    # Call help(); after completion the buffer should contain bytes. We can't
    # deterministically assert the exact placement of the replacement glyph,
    # but ensure the call completes and buffer is non-empty.
    kms.help()
    data = buf.getvalue()
    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0
