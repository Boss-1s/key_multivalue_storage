#!/bin/bash

# Suggested that
# source .venv/bin/activate
# is run first before running this script

# Optional, only if uv not installed
# pip install uv
# uv venv
trap 'echo "Warning: the current script has disabled usage of Ctrl+C - to stop, use Ctrl+Z instead"' INT


uv sync --dev

export SSH_PRIVATE_KEY="" # Enter your private key here

python test reset_env "$SSH_PRIVATE_KEY" "username" "useremail"

pre-commit install

gh auth login --scopes "repo,workflow,write:discussion,admin:repo_hook,admin:org,admin:public_key,admin:org_hook,user,project,gist,read:packages,write:packages,delete:packages,codespace"

echo "You're all set! You can now develop for kms in VSCode!"

git restore vscode.sh
