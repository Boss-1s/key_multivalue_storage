import json
import subprocess

with open('.devcontainer/devcontainer.json', 'r') as f:
    data = json.load(f)

for extension_id in data['customizations']['vscode']['extensions']:
    print(extension_id)
    subprocess.run(["code", "--install-extension", extension_id], capture_output=True, check=True)
