#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository. Run 'git init' first."
  exit 1
fi

git config core.hooksPath .githooks
echo "Git hooks enabled: core.hooksPath=.githooks"
