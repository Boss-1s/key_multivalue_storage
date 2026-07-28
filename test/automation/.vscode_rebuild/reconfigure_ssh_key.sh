#!/bin/bash

bash .github/workflows/src/ssh.sh

git config --global core.sshCommand "ssh -i ~/.ssh/id_ed25519"

echo ''
echo 'Testing connection...'

ssh -T git@github.com

exit 0