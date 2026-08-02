"""
Find diffs using griffe.
Most likely will be in the dev package env on pip.

NOTE: 75% AI-generated
"""

import sys
import warnings
try:
    import griffe #type: ignore
except ImportError:
    print("Could not find package griffe. Did you run `uv sync --dev`?")
    sys.exit(1)

try:
    RICH = True
    from rich.console import Console
    from rich import print #pylint: disable=redefined-builtin
    from rich.traceback import install
except ImportError:
    RICH = False
    warnings.warn("Warning: Rich is not installed. Pretty printing is not avaliable.")

from os import environ
from typing import Any
from griffe import load_git #type: ignore

def check_git_breaking_changes(package_name: str, old_ref: str, new_ref: str):
    """Find breaking changes between two refs"""
    print(f"[blue]Loading package state at {old_ref}...[/]")
    old_api = load_git(package_name, ref=old_ref, repo=".", search_paths=["src"])

    print(f"[blue]Loading package state at {new_ref}...[/]")
    new_api = load_git(package_name, ref=new_ref, repo=".", search_paths=["src"])

    print("\n[cyan]--- Breaking Changes Found ---[/]")
    breakages = list(griffe.find_breaking_changes(old_api, new_api))

    if not breakages:
        print("[green bold]Success: No breaking changes detected between these commits![/]")
        return

    for breakage in breakages:
        print(breakage.explain())

def find_breaking_changes(package_name: str, git_ref: Any):
    """Find breaking changes between the CWD against a historical tag"""
    print(f"[blue]Loading historical package state from Git commit/ref: {git_ref}...[/]")
    old_api = load_git(package_name, ref=git_ref, repo=".", search_paths=["src"])
    new_api = griffe.load("key_multivalue_storage")

    print("\n[cyan]--- Breaking Changes Found ---[/]")
    breakages = list(griffe.find_breaking_changes(old_api, new_api))

    if not breakages:
        print("[green b]Success: No breaking changes detected![/]")
        return

    for breakage in breakages:
        print(breakage.explain())

if __name__ == "__main__":
    if RICH:
        console = Console()
        install(console=console, show_locals=True)


    PACKAGE_NAME = "key_multivalue_storage" # The name of the module/package inside the git repo

    if environ.get("diff_py_tworef", None):
        check_git_breaking_changes(PACKAGE_NAME,
                                   environ.get('OLDTAG','v1.3.0.20260523a0'),
                                   environ.get('NEWTAG','v1.3.0.20260727rc1')
        )
    else:
        find_breaking_changes(PACKAGE_NAME, environ.get('OLDTAG','v1.3.0.20260727rc1'))
