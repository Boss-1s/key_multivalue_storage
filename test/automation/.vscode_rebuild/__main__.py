import subprocess
import time

subprocess.run(["python","test/automation/.vscode_rebuild/reinstall_extensions.py"], check=True)
time.sleep(1)
subprocess.run(["bash","test/automation/.vscode_rebuild/reconfigure_ssh_key.sh"], check=True)
