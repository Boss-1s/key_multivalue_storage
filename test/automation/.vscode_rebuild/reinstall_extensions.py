import re
import json
import subprocess

with open('.devcontainer/devcontainer.json', 'r') as f:
    file = f.read()

re.sub(r'(?:^|\s+)//.*$', '', code_snippet, flags=re.MULTILI)

for extension_id in data['customizations']['vscode']['extensions']:
    print(extension_id)
    subprocess.run(["code", "--install-extension", extension_id], capture_output=True, check=True)
