#!/bin/bash

git pull origin $BRANCH

# Capture the output of git status --porcelain
GIT_STATUS_OUTPUT=$(git status --porcelain)

# Check if the output is empty
if [ -z "$GIT_STATUS_OUTPUT" ]; then
  echo "Git working tree is clean (no uncommitted changes)."
  exit 0
else
  echo "Git working tree has uncommitted changes:"
  echo "$GIT_STATUS_OUTPUT"
  echo "These changes will be pushed to the $BRANCH branch."
fi

git add .
git restore --staged .github/.tmp/
git commit -m "[Release] Update file version"
git push origin $BRANCH
