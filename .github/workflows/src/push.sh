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

git add .
git restore --staged .github/.tmp/
git commit -m "[Release] Update file version"

if [ $DUMMY == "true" ]; then
  echo "git push to origin/$BRANCH here"
else
  git push origin $BRANCH
fi
