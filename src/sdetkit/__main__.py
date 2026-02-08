from __future__ import annotations

import argparse
import json
import sys


def _cassette_get(argv: list[str]) -> int:
    import httpx

    from .cassette import Cassette, CassetteRecordTransport, CassetteReplayTransport

    ap = argparse.ArgumentParser(prog="sdetkit cassette-get")
    ap.add_argument("url")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--record", metavar="PATH")
    g.add_argument("--replay", metavar="PATH")
    ns = ap.parse_args(argv)

    url: str = ns.url
    record: str | None = ns.record
    replay: str | None = ns.replay

    if replay:
        cass = Cassette.load(replay)
        transport = CassetteReplayTransport(cass)
        with httpx.Client(transport=transport) as client:
            r = client.get(url)
            r.raise_for_status()
            sys.stdout.write(json.dumps(r.json(), ensure_ascii=True))
        f = getattr(transport, "assert_exhausted", None)
        if callable(f):
            f()
        return 0

    if record:
        cass = Cassette()
        inner = httpx.HTTPTransport()
        transport = CassetteRecordTransport(cass, inner)
        with httpx.Client(transport=transport) as client:
            r = client.get(url)
            r.raise_for_status()
            sys.stdout.write(json.dumps(r.json(), ensure_ascii=True))
        cass.save(record)
        return 0

    with httpx.Client() as client:
        r = client.get(url)
        r.raise_for_status()
        sys.stdout.write(json.dumps(r.json(), ensure_ascii=True))
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] == "cassette-get":
        try:
            return _cassette_get(argv[1:])
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1

    from .cli import main as cli_main

    return int(cli_main() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
