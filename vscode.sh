#!/bin/bash

pip install uv
uv venv && uv sync --dev
source .venv/bin/activate

export SSH_PRIVATE_KEY="" # Enter your private key here

python test reset_env "$SSH_PRIVATE_KEY" "user.name" "user.email" || true
python test reset_env "$SSH_PRIVATE_KEY" "user.name" "user.email" #run twice bc python-enviroment will KeyboardInterrupt

gh auth login --scopes "repo,workflow,write:discussion,admin:repo_hook,admin:org,admin:public_key,admin:org_hook,user,project,gist,read:packages,write:packages,delete:packages,codespace"

echo "You're all set! You can now develop for kms in VSCode!"

git restore vscode.sh
