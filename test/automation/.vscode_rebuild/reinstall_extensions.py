import json
import subprocess

with open('.devcontainer/devcontainer.json', 'r') as f:
    data = json.load(f)

for extension_id in data['customizations']['vscode']['extensions']:
    try:
        print(f"Installing extension: {extension_id}")
        subprocess.run(["code", "--install-extension", extension_id, "--force"],
                    check=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
    except KeyboardInterrupt:
        pass

print("Installation complete. Check the Extensions tab to verify that all extensions have been",
      "installed successfully.")
