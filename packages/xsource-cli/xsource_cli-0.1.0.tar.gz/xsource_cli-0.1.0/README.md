# XSource Security CLI

MCP & AI Agent Security Scanner

## Installation

```bash
# Recommended (works on Kali, Ubuntu, etc.)
pipx install git+https://github.com/XSource-Sec/xsource-cli.git

# Or with venv
python3 -m venv venv && source venv/bin/activate
pip install git+https://github.com/XSource-Sec/xsource-cli.git
```

## Quick Start

```bash
xsource scan --demo https://vulnerable-mcp-demo.fly.dev/mcp
# → 26 vulnerabilities (12 CRITICAL, 5 HIGH, 7 MEDIUM, 2 LOW)
```

## Full Usage (requires account)

```bash
xsource login
xsource scan https://your-mcp-server.com/mcp
xsource report export 123 --format pdf
```

## License

MIT
