#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if [ ! -d ".venv/bin" ]; then
  echo "Missing .venv/bin. Create venv and install deps first." >&2
  exit 1
fi

export PATH="$repo_root/.venv/bin:$PATH"
echo "PATH updated for this shell: $repo_root/.venv/bin"
exec "${SHELL:-/bin/bash}" -i
