from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zip_deterministic(output: Path, files: list[Path], base: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(files, key=lambda p: p.as_posix()):
            rel = fp.relative_to(base).as_posix()
            info = zipfile.ZipInfo(rel)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, fp.read_bytes())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sdetkit evidence")
    sub = p.add_subparsers(dest="cmd", required=True)
    pack = sub.add_parser("pack")
    pack.add_argument("--output", default=".sdetkit/out/evidence.zip")
    ns = p.parse_args(argv)

    out_dir = Path(".sdetkit/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "doctor.txt",
        "repo-audit.json",
        "security.sarif",
        "sbom.cdx.json",
        "policy-snapshot.json",
        "policy-diff.json",
        "manifest.json",
        "evidence-errors.log",
    ]:
        target = out_dir / name
        if target.exists():
            target.unlink()

    commands = [
        (["python3", "-m", "sdetkit", "doctor", "--ascii"], out_dir / "doctor.txt"),
        (
            [
                "python3",
                "-m",
                "sdetkit",
                "repo",
                "audit",
                ".",
                "--format",
                "json",
                "--fail-on",
                "none",
                "--output",
                str(out_dir / "repo-audit.json"),
            ],
            None,
        ),
        (
            [
                "python3",
                "-m",
                "sdetkit",
                "security",
                "scan",
                "--fail-on",
                "none",
                "--format",
                "sarif",
                "--output",
                str(out_dir / "security.sarif"),
                "--sbom-output",
                str(out_dir / "sbom.cdx.json"),
            ],
            None,
        ),
        (
            [
                "python3",
                "-m",
                "sdetkit",
                "policy",
                "snapshot",
                "--output",
                str(out_dir / "policy-snapshot.json"),
            ],
            None,
        ),
    ]

    for cmd, capture_path in commands:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if capture_path is not None:
            capture_path.write_text((proc.stdout or "") + (proc.stderr or ""), encoding="utf-8")
        if proc.returncode != 0:
            err_log = out_dir / "evidence-errors.log"
            prefix = err_log.read_text(encoding="utf-8") if err_log.exists() else ""
            err_log.write_text(prefix + f"failed: {' '.join(cmd)}\n", encoding="utf-8")

    baseline = Path(".sdetkit/policies/baseline.json")
    if baseline.is_file():
        proc = subprocess.run(
            [
                "python3",
                "-m",
                "sdetkit",
                "policy",
                "diff",
                "--baseline",
                str(baseline),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        (out_dir / "policy-diff.json").write_text(proc.stdout, encoding="utf-8")

    files = [
        p
        for p in out_dir.iterdir()
        if p.is_file() and p.name != "manifest.json" and p.name != Path(ns.output).name
    ]
    manifest = {
        "version": 1,
        "files": [{"path": p.name, "sha256": _sha(p)} for p in sorted(files, key=lambda i: i.name)],
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    files.append(out_dir / "manifest.json")

    _zip_deterministic(Path(ns.output), files, out_dir)
    sys.stdout.write(f"{ns.output}\n")
    return 0
