# Public release verification records

This page is the repository's **post-release credibility log**.

Use it only for real, completed verification runs after a tag is published and the release workflow succeeds. Do not pre-fill this page with hypothetical results.

## Status

No public release verification record has been added yet.

When the first successful external install verification is completed, add an entry in the format below.

## Minimal evidence format (copy for each released version)

```md
### vX.Y.Z — YYYY-MM-DD

- Package/version verified: `sdetkit==X.Y.Z`
- Verifier: <maintainer-handle>
- Environment:
  - OS: <e.g., Ubuntu 24.04>
  - Python: <e.g., 3.11.11>
  - Installer: <e.g., pip 25.0>

Install and verification commands run:

```bash
python -m venv .venv-release-verify
. .venv-release-verify/bin/activate
python -m pip install -U pip
python -m pip install sdetkit==X.Y.Z
python -m sdetkit --help
python -m pip show sdetkit
```

Success signals captured:

- `pip install` resolved from default PyPI index.
- `python -m sdetkit --help` exited 0.
- `python -m pip show sdetkit` reported `Version: X.Y.Z`.
- PyPI page: <https://pypi.org/project/sdetkit/X.Y.Z/> reachable.
- GitHub Release: <release-url> contains expected artifacts.

Failure/support path:

- If install fails, open a bug using the issue tracker and include OS, Python, pip version, full install output, and command history.
```

## Evidence quality bar (lightweight)

Each entry should include only the essentials external users care about:

1. Exact released package version.
2. Exact install command.
3. Environment details (OS/Python/pip).
4. One post-install command proving usability (`python -m sdetkit --help`).
5. Plain success signals and where to report failures.

This keeps verification credible without adding heavy release bureaucracy.
