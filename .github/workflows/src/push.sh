#!/usr/bin/env bash

# 1. Configure the GitHub Actions Bot
git config --global user.name "github-actions[bot]"
git config --global user.email "41898282+github-actions[bot]@://github.com"

# 2. Stage changes and safely isolate your tmp directory
git add .
git restore --staged .github/.tmp 2>/dev/null || true

# 3. Check current status after optimization
GIT_STATUS_OUTPUT=$(git status --porcelain)

if [ -z "$GIT_STATUS_OUTPUT" ]; then
  echo "Git working tree is clean. No version changes to commit."
  exit 0
fi

echo "Git working tree has uncommitted changes:"
echo "$GIT_STATUS_OUTPUT"
echo "Pushing changes directly to the remote branch: $BRANCH"

# 4. Commit and push directly using HEAD to bypass detached HEAD state
git commit -m "[Release] Update file version [skip ci]"
git push origin HEAD:$BRANCH
