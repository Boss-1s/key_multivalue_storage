"""
[Precommit Code, please do not use in production]
Module that automatically does precommit cleanup and file refactors
relating to the date or commit SHAs.
"""
import os
import re
import sys
import subprocess
from datetime import datetime
from git import Repo
from rich.console import Console

try:
    repo_root = os.environ.get("GITHUB_WORKSPACE",
                               os.path.abspath(os.path.join(__file__, "../../..")))
except NameError:
    repo_root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
metadata_path = os.path.join(repo_root, "src/key_multivalue_storage/utils/metadata.py")

def is_file_modified(file_path):
    """check if file modified with GitPython"""
    repo = Repo(os.getcwd())
    repo.git.add(file_path)
    diff = repo.git.diff('HEAD', file_path)
    return bool(diff)

class_to_module: dict[str, str] = {
    "_StorageMeta": "src/key_multivalue_storage/storage.py",
    "_LoadMeta": "src/key_multivalue_storage/load.py",
    "_EditMeta": "src/key_multivalue_storage/edit.py",
    "_DeleteMeta": "src/key_multivalue_storage/delete.py"
}

try:
    with open(metadata_path, "r+", encoding="utf-8") as f:
        f_lines = f.readlines()
        i = 0
        current_class: str = ''
        while i < len(f_lines):
            line = f_lines[i]
            print(f"Processing line #{i + 1} of {len(f_lines)}: '{line.strip()}'")
            if "class" in line:
                # Check if the line contains a class definition
                class_match = re.match(r'class\s+(\w+)\s*\(.*\)\s*:', line.strip())
                if class_match:
                    current_class = class_match.group(1)
                    print(f"Found class definition: {current_class}")

            if re.match(r'return "\d{4}/\d{2}/\d{2}"', line.strip()):
                if is_file_modified(class_to_module[current_class]):
                    f_lines[i] = (
                        f'        return "{datetime.now().year:04d}/'+
                        f'{datetime.now().month:02d}/{datetime.now().day:02d}"\n'
                )
            elif re.match(r'return "\d{4}.\d{2}.\d{2}"', line.strip()):
                if is_file_modified(class_to_module[current_class]):
                    f_lines[i] = (
                        f'        return "{datetime.now().year:04d}.'+
                        f'{datetime.now().month:02d}.{datetime.now().day:02d}"\n'
                )
            i += 1

        f.seek(0)
        f.writelines(f_lines)
        f.truncate()
        print("Completed job.")
        print("Staging changes...")
        subprocess.run(["git", "add", metadata_path], capture_output=True, check=True)
        sys.exit(0)
except Exception as e:
    console = Console()
    console.print_exception(show_locals=True)
    console.print(f"[b red]Error processing file '{metadata_path}': {e}")
    sys.exit(1)
