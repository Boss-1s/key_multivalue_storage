---
title: fix(help): make Console robust to legacy Windows encodings
---

Fixes #14

## Changes
- Make help() resilient to legacy Windows encodings by wrapping stdout with a UTF‑8 TextIOWrapper(errors='replace') when needed; fall back to a no-color Console if wrapper construction fails.
- Add test/test-help-encoding.py to verify kms.help() does not raise on simulated legacy cp1252 stdout and other edge cases.

## Testing
- Added unit tests that simulate legacy and UTF-8 stdout environments, as well as failures when accessing stdout.encoding and when TextIOWrapper construction fails.
- Please run Windows CI (windows-latest) to confirm behavior on an actual Windows runner.

### Test Environment:
- OS: N/A (tests simulate streams)
- Python Version: 3.14 (target)
- [x] A `venv` was used to test locally
