# Quick Start Guide

Get up and running with Prometheus MCP Server in 5 minutes.

## Prerequisites

- Python 3.12 or higher
- Prometheus server (local or remote)
- Claude Desktop (optional, for AI integration)

## 1. Install

### Option A: Using pipx (Recommended for CLI usage)

```bash
pipx install prometheus-mcp-server
```

### Option B: Using uv

```bash
uv pip install prometheus-mcp-server
```

### Option C: Using pip

```bash
pip install prometheus-mcp-server
```

### Option D: From source

```bash
git clone <repository-url>
cd prometheus-mcp-server
uv pip install -e .
```

## 2. Start Local Prometheus (Optional)

If you don't have a Prometheus server, start one locally:

```bash
# Quick start with Docker
docker run -d -p 9090:9090 prom/prometheus

# Or use the provided docker-compose
cd examples
docker-compose up -d
```

Verify Prometheus is running:

```bash
curl http://localhost:9090/-/healthy
# Should return: Prometheus is Healthy.
```

## 3. Configure Environment

Create a `.env` file or set environment variables:

```bash
# Required
export PROM_URL="http://localhost:9090"

# Optional: Authentication
export PROM_TOKEN="your_bearer_token"
# Or
export PROM_USERNAME="admin"
export PROM_PASSWORD="secret"
```

## 4. Test the Server

Run the server:

```bash
prometheus-mcp-server
```

You should see output indicating the server is running.

## 5. Use with Claude Desktop

### Configure Claude Desktop

Edit your Claude Desktop config file:

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

Add this configuration:

```json
{
  "mcpServers": {
    "prometheus": {
      "command": "prometheus-mcp-server",
      "env": {
        "PROM_URL": "http://localhost:9090"
      }
    }
  }
}
```

Or with authentication:

```json
{
  "mcpServers": {
    "prometheus": {
      "command": "prometheus-mcp-server",
      "env": {
        "PROM_URL": "https://prometheus.example.com",
        "PROM_TOKEN": "your_bearer_token",
        "PROM_TIMEOUT": "60"
      }
    }
  }
}
```

### Restart Claude Desktop

Restart Claude Desktop to load the new configuration.

## 6. Test with Claude

In Claude Desktop, try these prompts:

### Check Health
```
"Is my Prometheus server healthy?"
```

### List Metrics
```
"What metrics are available in Prometheus?"
```

### Query Current Status
```
"Show me which targets are up"
```

### Investigate Alerts
```
"Are there any active alerts?"
```

### Analyze Performance
```
"What's the CPU usage across all instances?"
```

## 7. Common Use Cases

### Check Service Health

```
User: "Is the API service healthy?"

AI will:
1. Check target status: query_instant(query='up{job="api"}')
2. Check error rate: query_instant(query='rate(http_requests_total{job="api",status=~"5.."}[5m])')
3. List any active alerts
```

### Investigate High Memory Alert

```
User: "The HighMemoryUsage alert is firing. Help investigate."

AI will:
1. List active alerts
2. Check current memory usage
3. Show memory trend over time
4. Identify which pods/containers are using most memory
```

### Find Top CPU Consumers

```
User: "Which pods are using the most CPU?"

AI will:
1. Query: topk(10, rate(container_cpu_usage_seconds_total[5m]))
2. Show results sorted by CPU usage
3. Optionally show trends
```

## Troubleshooting

### Server Won't Start

```bash
# Check Python version (must be 3.12+)
python --version

# Verify installation
prometheus-mcp-server --help

# Check Prometheus connectivity
curl $PROM_URL/-/healthy
```

### Connection Refused

```bash
# Check Prometheus is running
curl http://localhost:9090/-/healthy

# Check environment variable
echo $PROM_URL

# Test with explicit URL
prometheus-mcp-server --url http://localhost:9090
```

### Authentication Errors

```bash
# Test token
curl -H "Authorization: Bearer $PROM_TOKEN" \
  $PROM_URL/api/v1/query?query=up

# Test basic auth
curl -u $PROM_USERNAME:$PROM_PASSWORD \
  $PROM_URL/api/v1/query?query=up
```

### Claude Desktop Not Finding Server

1. Check the config file path is correct
2. Verify JSON syntax is valid
3. Ensure `prometheus-mcp-server` is in PATH
4. Restart Claude Desktop completely
5. Check Claude Desktop logs

## Next Steps

- Read the [full README](README.md) for detailed documentation
- Explore [examples](examples/) for different configurations
- Check [USER_STORIES.md](USER_STORIES.md) for all available features
- Review [TESTING.md](TESTING.md) for testing guidance

## Getting Help

- Check the [README](README.md) for comprehensive documentation
- Review [examples/README.md](examples/README.md) for configuration examples
- Open an issue on GitHub for bugs or feature requests

## Quick Reference

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PROM_URL` | Prometheus URL | `http://localhost:9090` |
| `PROM_TOKEN` | Bearer token | `eyJhbG...` |
| `PROM_USERNAME` | Basic auth user | `admin` |
| `PROM_PASSWORD` | Basic auth password | `secret` |
| `PROM_TIMEOUT` | Request timeout (seconds) | `30` |
| `PROM_VERIFY_SSL` | Verify SSL certs | `true` |

### CLI Arguments

```bash
# Basic usage
prometheus-mcp-server

# With authentication
prometheus-mcp-server --url https://prometheus.example.com --token TOKEN

# HTTP transport for testing
prometheus-mcp-server --transport http --port 8000

# Disable SSL verification (not recommended)
prometheus-mcp-server --no-verify-ssl
```

### Available Tools (17 total)

**Queries:** query_instant, query_range, query_exemplars
**Metadata:** list_metrics, get_metric_metadata, list_labels, get_label_values, find_series
**Targets:** list_targets, get_targets_metadata
**Alerts:** list_alerts, list_rules
**Status:** get_config, get_flags, get_runtime_info, get_tsdb_stats, check_health, check_readiness

## Success Checklist

- [ ] Python 3.12+ installed
- [ ] prometheus-mcp-server installed
- [ ] Prometheus server accessible
- [ ] Environment variables configured
- [ ] Server runs without errors
- [ ] Claude Desktop config updated
- [ ] Claude Desktop restarted
- [ ] Successfully queried Prometheus via Claude

## All Set!

You're now ready to use Prometheus MCP Server with AI-powered monitoring investigation!

Try asking Claude about your Prometheus metrics, alerts, and infrastructure health.
