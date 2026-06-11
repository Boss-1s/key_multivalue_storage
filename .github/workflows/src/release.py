import os

# 1. Dynamically find the repo root using GitHub's default env variable
# Fallback to parent directories if running locally outside of GitHub Actions
try:
  repo_root = os.environ.get("GITHUB_WORKSPACE", os.path.abspath(os.path.join(__file__, "../../../..")))
except NameError:
  # If GITHUB_WORKSPACE exists, use it. Otherwise, use the directory you are currently in.
  repo_root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
pyproject_path = os.path.join(repo_root, "pyproject.toml")
init_py_path = os.path.join(repo_root, "src/key_multivalue_storage/__init__.py")
nightly = os.environ.get("NIGHTLY")
newv = os.environ.get("NVERSION")
newv_name = os.environ.get("RELEASENVERSION")

with open(pyproject_path, "r+") as f:
  pyproject = f.readlines()

  f.seek(0)
  
  for l in pyproject:
    if l.startswith('version = '):
      print(f"::notice:: release.py: replacing line '{l.replace('\n', '')}'")
      nl = f'version = "{newv}"\n'
      f.write(nl)
      print(f"::notice:: release.py: line is now '{nl.replace('\n', '')}'")
    elif l.startswith('    "Development Status :: '):
      print(f"::notice:: release.py: replacing line '{l.replace('\n', '')}'")
      if nightly:
        nl = f'    "Development Status :: 2 - Pre-Alpha",\n'
      elif 'a' in newv:
        nl = f'    "Development Status :: 3 - Alpha",\n'
      elif 'b' in newv:
        nl = f'    "Development Status :: 4 - Beta",\n'
      else:
        nl = f'    "Development Status :: 5 - Production/Stable",\n'
      f.write(nl)
      print(f"::notice:: release.py: line is now '{nl.replace('\n', '')}'")
    else:
      f.write(l)

  f.truncate()

with open(pyproject_path, "r") as f:
  print("New pyproject.toml file:\033[32m")
  print(f.read())
  print("\033[0m")

with open(init_py_path, "r+") as f:
  pyproject = f.readlines()

  f.seek(0)
  
  for l in pyproject:
    if l.startswith('__version__ = '):
      print(f"::notice:: release.py: replacing line '{l.replace('\n', '')}'")
      nl = f'__version__ = "{newv}"\n'
      f.write(nl)
      print(f"::notice:: release.py: line is now '{nl.replace('\n', '')}'")
    elif l.startswith('__version_internal__ = '):
      print(f"::notice:: release.py: replacing line '{l.replace('\n', '')}'")
      nl = f'__version_internal__ = "{newv_name}"\n'
      f.write(nl)
      print(f"::notice:: release.py: line is now '{nl.replace('\n', '')}'")
    else:
      f.write(l)

  f.truncate()

with open(init_py_path, "r") as f:
  print("New __init__.py file:\033[32m")
  print(f.read())
  print("\033[0m")
  
