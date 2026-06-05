#!/usr/bin/env bash

# Note: 5% AI-generated
set -e

SSH_REMOTE_URL=$(git remote get-url origin | sed -E 's|https://github.com/|git@github.com:|')

echo "Rewriting remote push origin target to: $SSH_REMOTE_URL"
git remote set-url origin "$SSH_REMOTE_URL"

git pull origin "$BRANCH"

GIT_STATUS_OUTPUT=$(git status --porcelain)

if [ -z "$GIT_STATUS_OUTPUT" ]; then
  echo "Git working tree is clean. No version changes to commit."
  exit 0
fi

git add .
git restore --staged .github/.tmp/
git commit -m "[Release] Update file version"

if [[ "$DUMMY" == "true" ]]; then
  git push origin "$BRANCH" --dry-run
  git reset --soft HEAD~1
  exit 0
else
  git push -u origin "$BRANCH"
fi

