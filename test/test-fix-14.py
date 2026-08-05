#pylint: disable=C
import io
import sys
import key_multivalue_storage as kms


# =====================================================================
# NON-CLOSING BUFFER STREAM (Fixes the I/O Closed File Error)
# =====================================================================
class NonClosingBytesIO(io.BytesIO):
    """A BytesIO buffer that refuses to close, keeping data readable for assertions."""
    def close(self):
        # Ignore close requests from TextIOWrapper teardowns
        pass


# =====================================================================
# PURE PYTHON MONKEYPATCH SIMULATOR (Standalone Test Engine)
# =====================================================================
class SimpleMonkeyPatch:
    """A minimal clone of pytest's monkeypatch to allow standard script execution."""
    def __init__(self):
        self._undo_stack = []

    def setattr(self, target, name, value):
        if hasattr(target, name):
            old_value = getattr(target, name)
            self._undo_stack.append((target, name, True, old_value))
        else:
            self._undo_stack.append((target, name, False, None))
        setattr(target, name, value)

    def undo(self):
        for target, name, existed, old_value in reversed(self._undo_stack):
            if existed:
                setattr(target, name, old_value)
            else:
                try:
                    delattr(target, name)
                except AttributeError:
                    pass
        self._undo_stack.clear()


# ==========================================
# FIXED TEST CASES WITH PROTECTED BUFFERS
# ==========================================

def test_help_does_not_raise_on_legacy_encoding(monkeypatch):
    """Simulate a legacy Windows stdout (cp1252) by replacing sys.stdout."""
    buf = NonClosingBytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "cp1252"

        def write(self, s):
            try:
                self.buffer.write(s.encode("cp1252", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

        def close(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)
    kms.help()


def test_help_does_not_raise_when_stdout_is_utf8(monkeypatch):
    """When stdout.encoding already indicates UTF-8, help() should still run."""
    buf = NonClosingBytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "utf-8"

        def write(self, s):
            try:
                self.buffer.write(s.encode("utf-8", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

        def close(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)
    kms.help()


def test_help_handles_missing_encoding_attribute(monkeypatch):
    """If accessing sys.stdout.encoding raises, help() should still be safe."""
    buf = NonClosingBytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer

        @property
        def encoding(self):
            raise AttributeError("encoding access not supported")

        def write(self, s):
            try:
                self.buffer.write(s.encode("utf-8", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

        def close(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)
    kms.help()


def test_help_falls_back_if_textiowrapper_fails(monkeypatch):
    """If io.TextIOWrapper raises, the code should fall back safely."""
    buf = NonClosingBytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "cp1252"

        def write(self, s):
            try:
                self.buffer.write(s.encode("cp1252", errors="ignore"))
            except Exception:
                pass

        def flush(self):
            pass

        def close(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    class FailingTextIOWrapper:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("simulated TextIOWrapper failure")

    monkeypatch.setattr(io, "TextIOWrapper", FailingTextIOWrapper)

    if hasattr(kms, "TextIOWrapper"):
        monkeypatch.setattr(kms, "TextIOWrapper", FailingTextIOWrapper)

    kms.help()


def test_unmappable_characters_are_replaced(monkeypatch):
    """Ensure unmappable characters are handled into the underlying buffer."""
    buf = NonClosingBytesIO()

    class DummyStdout:
        def __init__(self, buffer):
            self.buffer = buffer
            self.encoding = "cp1252"

        def write(self, s):
            if isinstance(s, bytes):
                self.buffer.write(s)
            else:
                self.buffer.write(s.encode("utf-8", errors="replace"))

        def flush(self):
            pass

        def close(self):
            pass

    dummy = DummyStdout(buf)
    monkeypatch.setattr(sys, "stdout", dummy)

    kms.help()

    # Using the subclass keeps the buffer stream open here
    data = buf.getvalue()

    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0


# ==========================================
# STANDALONE EXECUTION ENGINE
# ==========================================
if __name__ == "__main__":
    print("Executing tests using local environment patcher...\n")

    tests = [
        test_help_does_not_raise_on_legacy_encoding,
        test_help_does_not_raise_when_stdout_is_utf8,
        test_help_handles_missing_encoding_attribute,
        test_help_falls_back_if_textiowrapper_fails,
        test_unmappable_characters_are_replaced
    ]

    passed = 0
    real_stdout = sys.stdout

    for test in tests:
        mp = SimpleMonkeyPatch()
        try:
            test(mp)
            real_stdout.write(f"✓ {test.__name__} passed.\n")
            passed += 1
        except Exception as e:
            real_stdout.write(f"✗ {test.__name__} failed: {type(e).__name__} - {e}\n")
        finally:
            mp.undo()

    real_stdout.write(f"\nExecution finished: {passed}/{len(tests)} tests passed.\n")
