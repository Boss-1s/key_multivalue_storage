"""
[Precommit Code, please do not use in production]
Module that automatically does precommit cleanup and file refactors
relating to the date or commit SHAs.
"""
import os
import re
import sys
from datetime import datetime
from rich.console import Console

try:
    repo_root = os.environ.get("GITHUB_WORKSPACE",
                               os.path.abspath(os.path.join(__file__, "../../..")))
except NameError:
    repo_root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
metadata_path = os.path.join(repo_root, "src/key_multivalue_storage/utils/metadata.py")

try:
    with open(metadata_path, "r+", encoding="utf-8") as f:
        f_lines = f.readlines()
        i = 0
        while i < len(f_lines):
            line = f_lines[i]
            print(f"Processing line #{i + 1} of {len(f_lines)}: '{line.strip()}'")
            if re.match(r'return "\d{4}/\d{2}/\d{2}"', line.strip()):
                f_lines[i] = (
                    f'        return "{datetime.now().year:04d}/'+
                    f'{datetime.now().month:02d}/{datetime.now().day:02d}"\n'
                )
            elif re.match(r'return "\d{4}.\d{2}.\d{2}"', line.strip()):
                f_lines[i] = (
                    f'        return "{datetime.now().year:04d}.'+
                    f'{datetime.now().month:02d}.{datetime.now().day:02d}"\n'
                )
            i += 1

        f.seek(0)
        f.writelines(f_lines)
        f.truncate()
        print("Completed job.")
        sys.exit(0)
except Exception as e:
    console = Console()
    console.print_exception(show_locals=True)
    console.print(f"[b red]Error processing file '{metadata_path}': {e}")
    sys.exit(1)
