import os

# 1. Dynamically find the repo root using GitHub's default env variable
# Fallback to parent directories if running locally outside of GitHub Actions
repo_root = os.environ.get("GITHUB_WORKSPACE", os.path.abspath(os.path.join(__file__, "../../../..")))
pyproject_path = os.path.join(repo_root, "pyproject.toml")
newv = os.environ.get("NVERSION")

with open(pyproject_path, "r+") as f:
  pyproject = f.readlines()

  f.seek(0)
  
  for l in pyproject:
    if l.startswith('version = '):
      print(f"release.py: 9:: INFO: replacing line '{l.replace('\n', '')}'")
      nl = f'version = "{newv}"\n'
      f.write(nl)
      print(f"release.py: 11:: INFO: line is now '{nl.replace('\n', '')}'")
    else:
      f.write(l)

  f.truncate()

with open(pyproject_path, "r") as f:
  print("New pyproject.toml file:")
  print(f.read())
