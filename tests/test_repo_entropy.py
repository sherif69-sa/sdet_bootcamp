from __future__ import annotations

import math

from sdetkit.repo import _shannon_entropy


def test_shannon_entropy_known_strings() -> None:
    assert _shannon_entropy("aaaa") == 0.0
    assert math.isclose(_shannon_entropy("ab"), 1.0, rel_tol=1e-12)

    mixed = _shannon_entropy("aab")
    assert 0.9 < mixed < 0.92

    uniform = _shannon_entropy("abcd")
    assert math.isclose(uniform, 2.0, rel_tol=1e-12)


def test_shannon_entropy_empty_string_regression() -> None:
    assert _shannon_entropy("") == 0.0


def test_shannon_entropy_handles_long_strings() -> None:
    token = "abc123XYZ_-/+="
    long_s = token * 20_000

    entropy = _shannon_entropy(long_s)

    assert entropy >= 0.0
    assert entropy <= math.log2(len(set(token))) + 1e-12
