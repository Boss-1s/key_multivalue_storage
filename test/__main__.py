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
import argparse
import subprocess
from rich.console import Console

def main():
    """Main method for testing via command line"""
    if len(sys.argv) == 1 or any(
        item in ["a", "all"] for item in [item.lower() for item in sys.argv]
    ):
        exec(open("test/test-general.py").read(), globals())
        print("-"*30)
        exec(open("test/test-meta.py").read(), globals())
        print("-"*30)
        exec(open("test/test-exceptions.py").read(), globals())
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
            sys.argv[2]
        except IndexError as e:
            raise ValueError(
                "Please provide a git commit/tag/branch to compare against the current branch."
            ) from e
        print("Finding breaking changes!")
        os.environ["OLDTAG"] = sys.argv[2]
        exec(open("test/diff.py").read(), globals())
        return
    if sys.argv[1].lower() == "help_shortcut":
        exec("import key_multivalue_storage as kms; kms.help()", globals())
        return
    raise ValueError(
        "Invalid argument. Available arguments: a, all, general, meta, diff, "+
        "exceptions, warnings, help_shortcut"
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console = Console()
        console.print_exception(show_locals=True)
        console.print(f"[b red]Error: {e}")
