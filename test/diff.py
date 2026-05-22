"""
Find diffs using griffe.
Most likely will be in the dev package env on pip.

Note: 98% AI-generated
"""

import sys
try:
    import griffe
except ImportError:
    print("Please download the dev package with",
          "'pip install key_multivalue_storage[dev]'",
          "to use this feature.")
    sys.exit(1)
from griffe import load_git
from pathlib import Path

def find_mismatched_breaking_changes(package_path: str, single_file_path: str):
    """Find breaking changes"""
    # 1. Load the original package
    # (Pointing to the directory containing __init__.py or the package folder)
    print("Loading original package...")
    old_api = griffe.load(package_path)

    # 2. Convert the single standalone file into an absolute path
    # Griffe requires a specific search path to isolate individual modules correctly
    new_file = Path(single_file_path).resolve()

    print("Loading standalone target file...")
    # 3. Load the single file by explicitly isolating its directory as the search path
    new_api = griffe.load(
        new_file.stem,  # The module name (filename without .py)
        search_paths=[new_file.parent]  # Force Griffe to look ONLY in that folder
    )

    # 4. Check for breaking changes
    print("\n--- Finding Breaking Changes ---")
    breakages = list(griffe.find_breaking_changes(old_api, new_api))

    if not breakages:
        print("Success: No breaking changes detected!")
        return

    for breakage in breakages:
        # Use the built-in .explain() method to see the exact API shift
        print(breakage.explain())

def check_git_breaking_changes(package_path: str, old_ref: str, new_ref: str):
    print(f"Loading package state at {old_ref}...")
    old_api = load_git(package_path, ref=old_ref)

    print(f"Loading package state at {new_ref}...")
    new_api = load_git(package_path, ref=new_ref)

    print("\n--- Finding Breaking Changes ---")
    breakages = list(griffe.find_breaking_changes(old_api, new_api))

    if not breakages:
        print("Success: No breaking changes detected between these commits!")
        return

    for breakage in breakages:
        print(breakage.explain())

def check_git_vs_standalone_file(package_name: str, git_ref: str, local_file_path: str):
    # 1. Load the package as it existed in a specific git commit/tag/branch
    print(f"Loading historical package state from Git commit/ref: {git_ref}...")
    old_api = load_git(package_name, ref=git_ref, repo=".", search_paths=["src"])

    # 2. Map the local standalone file into Griffe
    new_file = Path(local_file_path).resolve()

    print(f"Loading standalone target file: {new_file.name}...")
    # Force Griffe to read only this single file by setting its directory as the search path.
    # The module spec name MUST align with the base package name (or the specific
    # submodule name being tracked) for Griffe's internal map to match them up.
    new_api = griffe.load(
        package_name,          # Aligns the 'new' object map key with the 'old' one
        search_paths=[new_file.parent]  # Confines the loader to this specific folder
    )

    # 3. Analyze for breaking changes
    print("\n--- Finding Breaking Changes ---")
    breakages = list(griffe.find_breaking_changes(old_api, new_api))

    if not breakages:
        print("Success: No breaking changes detected!")
        return

    for breakage in breakages:
        print(breakage.explain())

if __name__ == "__main__":
    # Define your historical package identity and the loose file to check against it
    PACKAGE_NAME = "key_multivalue_storage"     # The name of the module/package inside the git repo
    GIT_COMMIT = "v1.2.2.20260506.2"         # The commit hash, tag, or branch representing the old code
    LOCAL_FILE = "./src/key_multivalue_storage/key_multivalue_storage.py"     # Path to the single modified file on your machine

    check_git_vs_standalone_file(PACKAGE_NAME, GIT_COMMIT, LOCAL_FILE)
