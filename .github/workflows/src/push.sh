#!/usr/bin/env bash

# Note: 5% AI-generated

if [ -z "$CUSTOM_COMMIT_MSG" ]; then
  echo "CUSTOM_COMMIT_MSG environment variable is not set. Setting to default 'commit'."
  CUSTOM_COMMIT_MSG="commit"
fi

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
git commit -m "[skip ci] release: $CUSTOM_COMMIT_MSG" -m "This commit is standard release procedure and was automatically commited as part of a release. This commit was created and pushed by automation."

if [[ "$DUMMY" == "true" ]]; then
  git push origin "$BRANCH" --dry-run
  git reset --soft HEAD~1
  exit 0
else
  git push -u origin "$BRANCH"
fi

