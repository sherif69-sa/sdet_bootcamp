import sys
from pathlib import Path

bad = []

bad.extend([str(p) for p in Path("docs/roadmap/plans").glob(".*.json")])

legacy_root = [
    ".gitlab-ci.day66-advanced-reference.yml",
    ".jenkins.day67-advanced-reference.Jenkinsfile",
    ".tekton.day68-self-hosted-reference.yaml",
]
bad.extend([f"forbidden: {p}" for p in legacy_root if Path(p).exists()])

required_templates = [
    "templates/ci/gitlab/day66-advanced-reference.yml",
    "templates/ci/jenkins/day67-advanced-reference.Jenkinsfile",
    "templates/ci/tekton/day68-self-hosted-reference.yaml",
]
bad.extend([f"missing: {p}" for p in required_templates if not Path(p).exists()])

if bad:
    sys.stderr.write("Repo layout invariant violations:\n" + "\n".join(bad) + "\n")
    raise SystemExit(1)

print("ok: repo layout invariants hold")
