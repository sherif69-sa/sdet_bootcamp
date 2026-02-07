# Source this file to put the repo venv scripts on PATH.
# Example:
#   cd ~/sdet_bootcamp
#   source scripts/env.sh
#   apigetcli --help

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -d "$repo_root/.venv/bin" ]; then
  export PATH="$repo_root/.venv/bin:$PATH"
fi
