#!/bin/bash

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
git config --global user.name "Boss-1s"
git config --global user.email "95505913+Boss-1s@users.noreply.github.com"

# Add Allowed Signers Configuration
git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
mkdir -p ~/.config/git
echo "$(git config user.email) $(cat ~/.ssh/id_ed25519.pub)" >> ~/.config/git/allowed_signers