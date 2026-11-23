# Intelligence Agent

This exercise now uses local agent skills instead of MCP servers.

## Setup

1. Set the required environment variables:

```bash
export VIRUSTOTAL_API_KEY=...
export GOOGLE_API_KEY=...
export RAPID_API_KEY=...
export OPENCVE_USERNAME=...
export OPENCVE_PASSWORD=...
```

2. If you are starting from a fresh directory, initialize the project and add the dependencies:

```bash
uv init
uv add fast-agent-mcp questionary requests
```

If the repository already includes `pyproject.toml` and `uv.lock`, you can skip the `uv init` and `uv add` steps.

## Run

From this directory, start the agent with:

```bash
uv run intelligence_client.py
```

Pick a model when prompted, then ask questions about:

- IP addresses
- domains
- URLs
- email addresses
- CVE or CWE identifiers

For email addresses, the orchestrator skill will run the DNS, URL, and email checks in order.

## Skills

The agent loads local skills from `skills/`:

- `network-intelligence`
- `dns-intelligence`
- `url-intelligence`
- `email-intelligence`
- `app-intelligence`
- `threat-intel-email-orchestrator`

Each skill runs a local Python helper script under its own `scripts/` directory.
