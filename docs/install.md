# Install SDETKit

This page is the canonical install guide for external users.

## Recommended install path (first-time users)

Install directly from GitHub, then verify the CLI:

```bash
python -m pip install "git+https://github.com/sherif69-sa/DevS69-sdetkit.git"
python -m sdetkit --help
```

Why this is the recommended path now:

- Works in any repository without cloning this project first.
- Uses the same public source every team can access.
- Does not rely on this repository's helper scripts.
- Public PyPI install is not yet verified in this repository's release records.

## Alternative install paths

Use these only if they better fit your environment.

### `pipx` (isolated CLI install)

```bash
pipx install "git+https://github.com/sherif69-sa/DevS69-sdetkit.git"
pipx run sdetkit --help
```

### `uv tool install` (isolated tool install)

```bash
uv tool install "git+https://github.com/sherif69-sa/DevS69-sdetkit.git"
uv tool run sdetkit --help
```

### Local source install (contributors in this repo)

```bash
python -m pip install .
python -m sdetkit --help
```

## First run in an external repository

From the root of the repository you want to gate:

```bash
python -m sdetkit gate fast
python -m sdetkit gate release
```

Start with `gate fast`, then add `gate release` when you want stricter release-confidence checks.

For rollout patterns and CI examples, continue with [Adopt SDETKit in your repository](adoption.md).

## Development setup (this repository only)

If you are contributing to SDETKit itself:

```bash
bash scripts/bootstrap.sh
source .venv/bin/activate
python -m pip install -e .[dev,test,docs]
```

This setup is for contributors/maintainers, not required for external adoption.

## PyPI/public distribution posture

SDETKit has release automation for build, wheel validation, optional PyPI publish, and provenance attestation in `.github/workflows/release.yml`.

Until a release is publicly published and externally verified, the install recommendation remains GitHub URL install.

- Maintainer release process summary: [Releasing sdetkit](releasing.md)
- Public verification log: [release-verification.md](release-verification.md)
