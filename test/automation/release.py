"""
[Release CI/CD Code, please do not use in production]
Module to dynamically change version and development status of package.
"""
import os

try:
    repo_root = os.environ.get("GITHUB_WORKSPACE",
                               os.path.abspath(os.path.join(__file__, "../../../..")))
except NameError:
    repo_root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
pyproject_path = os.path.join(repo_root, "pyproject.toml")
init_py_path = os.path.join(repo_root, "src/key_multivalue_storage/__init__.py")
nightly = os.environ.get("NIGHTLY")
newv = os.environ.get("NVERSION")
newv_name = os.environ.get("RELEASENVERSION")

with open(pyproject_path, "r+", encoding="utf-8") as f:
    pyproject = f.readlines()

    f.seek(0)

    for line in pyproject:
        if line.startswith('version = '):
            print(f"::notice:: release.py: replacing line '{line.replace('\n', '')}'")
            newline = f'version = "{newv}"\n'
            f.write(newline)
            print(f"::notice:: release.py: line is now '{newline.replace('\n', '')}'")
        elif line.startswith('    "Development Status :: '):
            print(f"::notice:: release.py: replacing line '{line.replace('\n', '')}'")
            if nightly:
                newline = '    "Development Status :: 2 - Pre-Alpha",\n'
            elif 'a' in str(newv):
                newline = '    "Development Status :: 3 - Alpha",\n'
            elif 'b' in str(newv):
                newline = '    "Development Status :: 4 - Beta",\n'
            else:
                newline = '    "Development Status :: 5 - Production/Stable",\n'
            f.write(newline)
            print(f"::notice:: release.py: line is now '{newline.replace('\n', '')}'")
        else:
            f.write(line)

    f.truncate()

with open(pyproject_path, "r", encoding="utf-8") as f:
    print("New pyproject.toml file:\033[32m")
    print(f.read())
    print("\033[0m")

with open(init_py_path, "r+", encoding='utf-8') as f:
    pyproject = f.readlines()

    f.seek(0)

    for line in pyproject:
        if line.startswith('__version__ = '):
            print(f"::notice:: release.py: replacing line '{line.replace('\n', '')}'")
            newline = f'__version__ = "{newv}"\n'
            f.write(newline)
            print(f"::notice:: release.py: line is now '{newline.replace('\n', '')}'")
        elif line.startswith('__version_internal__ = '):
            print(f"::notice:: release.py: replacing line '{line.replace('\n', '')}'")
            newline = f'__version_internal__ = "{newv_name}"\n'
            f.write(newline)
            print(f"::notice:: release.py: line is now '{newline.replace('\n', '')}'")
        else:
            f.write(line)

    f.truncate()

with open(init_py_path, "r", encoding='utf-8') as f:
    print("New __init__.py file:\033[32m")
    print(f.read())
    print("\033[0m")
