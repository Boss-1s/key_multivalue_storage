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
import argparse # TODO in kms-tester-semver0.1.0: better argument parsing
import subprocess
import warnings
from rich.console import Console
from rich.traceback import install

def main(c: Console) -> None:
    """Main method for testing via command line"""

    if len(sys.argv) == 1 or any(
        item in ["a", "all"] for item in [item.lower() for item in sys.argv]
    ):
        exec(open("test/test-general.py").read(), globals())
        c.print("-"*30)
        exec(open("test/test-meta.py").read(), globals())
        c.print("-"*30)
        exec(open("test/test-exceptions.py").read(), globals())
        c.print("-"*30)
        exec(open("test/test-fix-26-and-27.py").read(), globals())
        return
    if sys.argv[1].lower() == "general":
        exec(open("test/test-general.py").read(), globals())
        return
    if sys.argv[1].lower() == "meta":
        exec(open("test/test-meta.py").read(), globals())
        return
    if sys.argv[1].lower() in ["exceptions", "warnings"]:
        exec(open("test/test-exceptions.py").read(), globals())
        return
    if sys.argv[1].lower() == "diff":
        try:
            os.environ["OLDTAG"] = sys.argv[2]
        except IndexError:
            warnings.warn("No argument OLDTAG provided. Falling back to script default...")

        if os.environ.get("diff_py_tworef"): del os.environ["diff_py_tworef"]

        c.print("[green bold]Finding breaking changes![/]")
        exec(open("test/diff.py").read(), globals())
        return
    if sys.argv[1].lower() == "diff2":
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
        exec(open("test/diff.py").read(), globals())
        return
    if sys.argv[1].lower() == "help_shortcut":
        exec("import key_multivalue_storage as kms; kms.help()", globals())
        return
    if sys.argv[1].lower() == "reset_env":
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
        return

    raise ValueError(
        "Invalid argument. Available arguments: a, all, general, meta, diff, "+
        "exceptions, warnings, help_shortcut, reset_env"
    )

if __name__ == "__main__":
    console = Console()
    install(console=console, show_locals=True)
    main(console)
