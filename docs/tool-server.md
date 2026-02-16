# Tool server

`python -m sdetkit ops serve` starts a local HTTP/JSON server (localhost by default).

## Endpoints

- `GET /health`
- `GET /actions`
- `POST /run-action`
- `POST /run-workflow`
- `GET /runs`
- `GET /runs/<id>`

## Safety model

- Binds to `127.0.0.1` by default.
- Reuses the same workflow policy gates as CLI.
- Rejects invalid run IDs and traversal patterns.
