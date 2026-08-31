"""
Run all kms tests.

### Usage
In your terminal, run:
```sh
git clone https://github.com/boss-1s/key_multivalue_storage kms
cd kms
uv sync --dev
python test/
```
"""
#pylint: disable=exec-used,consider-using-with
import os
import sys
import time
import argparse # TODO in kms-tester-semver0.1.0: better argument parsing
import subprocess
import warnings
from rich.console import Console
from rich.traceback import install

def _run_tests(c: Console, tests: list[str]) -> None:
    total_tests = len(tests)
    tracebacks: list[Any] = []
    failed_tests: list[str] = []
    for test_file in tests:
        try:
            c.print(f"[blue]Running: {test_file}[/]")
            with open(test_file, "r", encoding='utf-8') as f:
                compiled_code = compile(f.read(), os.path.abspath(test_file), "exec")
                exec(compiled_code, globals())
            tracebacks.append(None)
        except Exception as e:
            print(f"❌ [red b]Error in {test_file}: {e}[/]")
            c.print_exception(show_locals=True)
            tracebacks.append(console.export_text())
            failed_tests.append(test_file)
            c.print(
                "[b][blue]Hint:[/b] hit Ctrl+Z/Ctrl+C to examine the issue more carefully[/]"
            )
            time.sleep(1.9)

        c.print("-" * 30)
        time.sleep(0.1)

    tracebacks = list(filter(lambda x: x is not None, tracebacks))
    
    c.print("[green b]All tests complete![/]")
    c.print("[blue]Final Statistics: [/]")
    c.print(f"[green]{total_tests - len(failed_tests)} of {total_tests} tests passed[/]")
    c.print(f"[red]Tracebacks:[/]\n{tracebacks}")
    if len(failed_tests) > 0:
        c.print(f"Failed Tests: {failed_tests}")
        sys.exit(1)

def main(c: Console) -> None:
    """Main method for testing via command line"""

    if len(sys.argv) == 1 or any(
        item in ["a", "all"] for item in [item.lower() for item in sys.argv]
    ):
        tests = [
            "test/test-storage.py",
            "test/test-load.py",
            "test/test-edit.py",
            "test/test-delete.py",
            "test/test-meta.py",
            "test/test-exceptions.py",
            "test/test-fix-26-and-27.py",
            "test/test-fix-14.py",
            "test/test-fix-67.py",
            "test/test-fix-76.py",
            "test/test-fix-80.py",
            "test/test-fix-84.py"
        ]

        _run_tests(c, tests)
        return

    match sys.argv[1].lower():
        case "general":
            try:
                if sys.argv[2].lower() == '1.3':
                    tests = [
                        "test/test-storage.py",
                        "test/test-load.py",
                        "test/test-edit.py",
                        "test/test-delete.py"
                    ]

                    _run_tests(c, tests)
            except IndexError:
                warnings.warn("You are using an OLD version of test-general, "+
                            "sepcifically the one targetd for kms-semver1.2.x.\n"+
                            "To run the new tests, run `python test/ general 1.3`.")
                _run_tests(c, ["test/test-general.py"])
        case "storage":
            _run_tests(c, ["test/test-storage.py"])
        case "load":
            _run_tests(c, ["test/test-load.py"])
        case "edit":
            _run_tests(c, ["test/test-edit.py"])
        case "delete":
            _run_tests(c, ["test/test-delete.py"])
        case "meta":
            _run_tests(c, ["test/test-meta.py"])
        case "exceptions" | "warnings":
            _run_tests(c, ["test/test-exceptions.py"])
        case "diff":
            try:
                os.environ["OLDTAG"] = sys.argv[2]
            except IndexError:
                warnings.warn("No argument OLDTAG provided. Falling back to script default...")

            if os.environ.get("diff_py_tworef"):
                del os.environ["diff_py_tworef"]

            c.print("[green bold]Finding breaking changes![/]")
            _run_tests(c, ["test/diff.py"])
        case "diff2":
            try:
                os.environ["OLDTAG"] = sys.argv[2]
            except IndexError:
                warnings.warn("No argument OLDTAG provided. Falling back to script default...")

            try:
                os.environ["NEWTAG"] = sys.argv[3]
            except IndexError:
                warnings.warn("No argument NEWTAG provided. Falling back to script default...")

            os.environ["diff_py_tworef"] = '1'
            c.print("[green bold]Finding breaking changes![/]")
            _run_tests(c, ["test/diff.py"])
        case "help_shortcut":
            exec("import key_multivalue_storage as kms; kms.help()", globals())
        case "reset_env":
            try:
                sys.argv[2]
            except IndexError as e:
                raise ValueError(
                    "Please provide a SSH private key to use."
                ) from e

            try:
                sys.argv[3]
            except IndexError as e:
                raise ValueError(
                    "Please provide a username for SSH-signed commits."
                ) from e

            try:
                sys.argv[4]
            except IndexError as e:
                raise ValueError(
                    "Please provide an email for SSH-signed commits."
                ) from e

            try:
                clearall = bool(sys.argv[5])
            except IndexError as e:
                clearall = False

            os.environ["SSH_PRIVATE_KEY"] = sys.argv[2]
            os.environ["SSH_USER"] = sys.argv[3]
            os.environ["SSH_EMAIL"] = sys.argv[4]
            os.environ["reconfig_ssh_key_clearall"] = str(int(clearall))
            subprocess.run(["python", "test/automation/.vscode_rebuild"], check=True)
        case _:
            raise ValueError(
                "Invalid argument. Available arguments: a, all, general, meta, diff, "+
                "exceptions, warnings, help_shortcut, reset_env"
            )

if __name__ == "__main__":
    console = Console()
    install(console=console, show_locals=True)
    main(console)
