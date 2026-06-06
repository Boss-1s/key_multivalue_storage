#!/bin/bash

git switch beta

git cherry-pick -Xtheirs 85d9f85^..b4b3924
