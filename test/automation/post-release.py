"""
[Release CI/CD Code, please do not use in production]
Module to dynamically bump past the current version into a dev version.
"""
import os
import argparse
from rich.traceback import install

def main():
    parser = argparse.ArgumentParser(description="Bump version in pyproject.toml and __init__.py")
    parser.add_argument("-v", "--version",
                        required=True,
                        type=str,
                        help="New version"
    )
    parser.add_argument("-n", "--name",
                        required=True,
                        type=str,
                        help="New version name")
    parser.add_argument("-d", "--dir_depth",
                        type=int,
                        default=4,
                        help="Depth of the directory to find the repo root")
    args = parser.parse_args()

    newv = args.version
    newv_name = args.name
    dir_depth = args.dir_depth

    try:
        repo_root = os.environ.get("GITHUB_WORKSPACE",
                                        os.path.abspath(
                                            os.path.join(__file__, "../"*dir_depth)
                                        )
        )
    except NameError:
        repo_root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    try:
        pyproject_path = os.path.join(repo_root, "pyproject.toml")
        init_py_path = os.path.join(repo_root, "src/key_multivalue_storage/__init__.py")

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
                    newline = '    "Development Status :: 2 - Pre-Alpha",\n'
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
    except FileNotFoundError as e:
        raise TypeError(str(e) + " -- Is your directory depth set correctly?") from e

if __name__ == "__main__":
    install(show_locals=True)
    main()
