#!/bin/bash

# TODO in kms-tester-semver0.1.0: GPG signing

if [ -z "$SSH_PRIVATE_KEY" ]; then
    echo "No SSH key provided. Please provide an SSH private key via the enviroment variable 'SSH_PRIVATE_KEY'."
    exit 1
fi

if [ -z "$SSH_EMAIL" ]; then
    echo "No email provided. Please provide an email via the enviroment variable 'SSH_EMAIL'."
    exit 1
fi

if [ -z "$SSH_USER" ]; then
    echo "No username provided. Please provide a username via the enviroment variable 'SSH_USER'."
    exit 1
fi

if [ -z "$reconfig_ssh_key_clearall" ]; then
    echo "Warning: The data passed WILL not be cleared. To clear the data, run this script with the env var reconfig_ssh_key_clearall set to true."
fi

# NOTE: AI-Generated

mkdir -p ~/.ssh

echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519

# Find the public key off the private key
ssh-keygen -y -f ~/.ssh/id_ed25519 > ~/.ssh/id_ed25519.pub

# Ensure ssh-agent recieves the key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-keyscan github.com >> ~/.ssh/known_hosts

# Git configurations for ssh
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global user.name "$SSH_USER"
git config --global user.email "$SSH_EMAIL"

# Add Allowed Signers Configuration
git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
mkdir -p ~/.config/git
echo "$(git config user.email) $(cat ~/.ssh/id_ed25519.pub)" >> ~/.config/git/allowed_signers

# End AI-Generated

git remote set-url origin git@github.com:Boss-1s/key_multivalue_storage.git

git config --global core.sshCommand "ssh -i ~/.ssh/id_ed25519"

echo ''
echo 'Testing connection...'

ssh -T git@github.com

if [ "$reconfig_ssh_key_clearall" ]; then
    echo "Clearing data..."
    export SSH_USER=''
    export SSH_EMAIl=''
    export SSH_PRIVATE_KEY=''
fi

exit 0