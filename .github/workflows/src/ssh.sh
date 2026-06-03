# NOTE: AI-Generated

mkdir -p ~/.ssh

echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519

ssh-keygen -y -f ~/.ssh/id_ed25519 > ~/.ssh/id_ed25519.pub

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-keyscan github.com >> ~/.ssh/known_hosts

git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global user.name "Boss-1s"
git config --global user.email "95505913+Boss-1s@users.noreply.github.com"
