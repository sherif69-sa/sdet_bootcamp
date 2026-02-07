# CLI

## kv
Reads key=value lines (stdin, --text, or --path) and prints JSON.

## apiget
Fetch JSON from a URL.

Examples:
- sdetkit apiget https://example.com/api --expect dict
- sdetkit apiget https://example.com/items --expect list --paginate --max-pages 50
- sdetkit apiget https://example.com/items --expect list --retries 3 --retry-429 --timeout 2
- sdetkit apiget https://example.com/items --expect list --trace-header X-Request-ID --request-id abc-123
