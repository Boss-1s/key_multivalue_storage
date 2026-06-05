#!/usr/bin/env bash

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
else
  git push -u origin "$BRANCH"
fi

