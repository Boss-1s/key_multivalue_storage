#!/usr/bin/env bash

# Note: 5% AI-generated

git remote set-url origin "git@github.com:Boss-1s/key_multivalue_storage.git"

git pull origin "$BRANCH"

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

if [[ "$DUMMY" == "true" ]]; then
  git push origin "$BRANCH" --dry-run
  git reset --soft HEAD~1
  exit 0
else
  git push -u origin "$BRANCH"
fi

