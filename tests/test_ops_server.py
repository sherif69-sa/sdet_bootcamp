from __future__ import annotations

import json
import threading
import time
import urllib.request
from pathlib import Path

import pytest

from sdetkit.ops import serve


@pytest.mark.network
def test_server_health_actions(tmp_path: Path) -> None:
    port = 8877
    thread = threading.Thread(target=serve, args=("127.0.0.1", port, tmp_path), daemon=True)
    thread.start()
    time.sleep(0.1)

    health = urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2).read()
    payload = json.loads(health.decode("utf-8"))
    assert payload["ok"] is True

    actions = urllib.request.urlopen(f"http://127.0.0.1:{port}/actions", timeout=2).read()
    ap = json.loads(actions.decode("utf-8"))
    assert any(item["name"] == "repo.audit" for item in ap["actions"])
