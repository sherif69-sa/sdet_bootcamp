# Blank repo to value in 60 seconds

This is the fastest honest proof path for a new visitor evaluating SDETKit in a fresh repository.

Goal: get a deterministic go/no-go signal plus machine-readable evidence in about a minute.

## 60-second command flow

```bash
python -m pip install "git+https://github.com/sherif69-sa/DevS69-sdetkit.git"
python -m sdetkit --help
python -m sdetkit doctor
python -m sdetkit gate fast --format json --stable-json --out build/gate-fast.json
python -m sdetkit gate release --format json --stable-json --out build/release-preflight.json
```

## What value you get immediately

1. **Environment confidence** via `doctor` before debugging random CI failures.
2. **Deterministic release-confidence checks** via `gate fast` and `gate release`.
3. **Structured evidence artifacts** in `build/` that can be uploaded to CI.

Expected artifact shape:

```text
build/
├── gate-fast.json
└── release-preflight.json
```

## How to read the first artifacts

### `build/gate-fast.json`

Look at:

- `ok`
- `failed_steps`
- `profile`

If `ok` is `false`, fix the first item in `failed_steps`, rerun, and repeat.

### `build/release-preflight.json`

Look at:

- `ok`
- `failed_steps`
- `profile`

If release preflight fails because `gate_fast` failed, start with `build/gate-fast.json` before reading long logs.

## Copy this into CI after local success

Start with PR checks:

```bash
python -m sdetkit gate fast
```

Then enforce stricter release checks on release branches:

```bash
python -m sdetkit security enforce --format json --max-error 0 --max-warn 0 --max-info 0 --out build/security-enforce.json
python -m sdetkit gate release --format json --stable-json --out build/release-preflight.json
```

## Related proof pages

- [Before/after evidence example](before-after-evidence-example.md)
- [SDETKit vs ad hoc scripts and separate tools](sdetkit-vs-ad-hoc.md)
- [Team rollout scenario](team-rollout-scenario.md)
