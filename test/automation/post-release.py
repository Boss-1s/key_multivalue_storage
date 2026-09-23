"""
[Release CI/CD Code, please do not use in production]
Module to dynamically bump past the current version into a dev version.
"""
import os
import argparse
import subprocess
import builtins
from rich.console import Console
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
    parser.add_argument("--test",
                        action="store_true",
                        default=False,
                        help="Run in test mode (dry-run)")
    parser.add_argument("--verbose",
                        action="store_true",
                        default=False,
                        help="Enable verbose output")
    args = parser.parse_args()

    newv: str = args.version
    newv_name: str = args.name
    og_v: str = ''
    dir_depth: int = args.dir_depth
    test_mode: bool = args.test
    verbose: bool = args.verbose

    console = Console(quiet=not verbose, force_terminal=True)

    print = console.print

    install(console=console, show_locals=verbose)

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

        print("[b blue]Diff pyproject.toml file:[/]")
        builtins.print(subprocess.run(["git", "--no-pager", "diff", "--color", pyproject_path], check=True, capture_output=True).stdout.decode("utf-8"))

        with open(init_py_path, "r+", encoding='utf-8') as f:
            pyproject = f.readlines()

            f.seek(0)

            for line in pyproject:
                if line.startswith('__version__ = '):
                    og_v = line.replace('\n', '').replace('__version__ = ', '').replace('"', '')
                    print(f"::notice:: release.py: replacing line '{og_v}'")
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

        print("[b blue]Diff __init__.py file:[/]")
        builtins.print(subprocess.run(["git", "--no-pager", "diff", "--color", init_py_path], check=True, capture_output=True).stdout.decode("utf-8"))
    except FileNotFoundError as e:
        raise TypeError(str(e) + " -- Is your directory depth set correctly?") from e
    except subprocess.CalledProcessError as e:
        raise SyntaxError(
            f"::error:: Internal error while attempting to diff files: {str(e)}"
        ) from e

    try:
        subprocess.run(["git", "add", pyproject_path, init_py_path],
                       check=True,
                       capture_output=True)
        subprocess.run(["git", "status"], check=True, capture_output=True)
        subprocess.run(["git",
                        "commit",
                        "-S",
                        "-s",
                        "-m",
                        f"release: post {og_v} [skip ci]",
                        "--dry-run" if test_mode else '--no-dry-run'],
                    check=True,
                    capture_output=True)
        subprocess.run(["git", "push", "--dry-run" if test_mode else '--no-dry-run'],
                    check=True,
                    capture_output=True)
    except Exception as e:
        raise SyntaxError(
            f"::error:: Internal error while attempting to commit: {str(e)}"
        ) from e
    finally:
        if test_mode:
            print("::notice:: release.py: Test mode enabled, nothing was commited or pushed.")
            subprocess.run(["git", "restore", "--staged", pyproject_path, init_py_path],
                           check=True,
                           capture_output=True)
            subprocess.run(["git", "restore", pyproject_path, init_py_path],
                           check=True,
                           capture_output=True)

    print("::notice:: release.py: Finished post-release version bumping.")


if __name__ == "__main__":
    main()
