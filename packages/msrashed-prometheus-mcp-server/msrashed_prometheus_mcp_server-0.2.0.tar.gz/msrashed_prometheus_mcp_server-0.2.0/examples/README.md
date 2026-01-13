# Prometheus MCP Server - Examples

This directory contains example configurations and setup files for testing and using the Prometheus MCP Server.

## Quick Start with Docker

### 1. Start Local Prometheus

```bash
cd examples
docker-compose up -d
```

This will start:
- **Prometheus** on http://localhost:9090
- **Node Exporter** on http://localhost:9100 (system metrics)
- **cAdvisor** on http://localhost:8080 (container metrics)

### 2. Verify Prometheus is Running

```bash
# Check if Prometheus is accessible
curl http://localhost:9090/api/v1/query?query=up

# Open Prometheus UI
open http://localhost:9090
```

### 3. Configure and Run MCP Server

```bash
# Set environment
export PROM_URL="http://localhost:9090"

# Run the server
prometheus-mcp-server
```

### 4. Stop Prometheus

```bash
docker-compose down

# To also remove volumes
docker-compose down -v
```

## Claude Desktop Configuration Examples

### Local Prometheus (Simplest)

File: `claude-desktop-config-local.json`

```json
{
  "mcpServers": {
    "prometheus-local": {
      "command": "prometheus-mcp-server",
      "env": {
        "PROM_URL": "http://localhost:9090"
      }
    }
  }
}
```

**Use case**: Testing with local Prometheus instance

### Remote Prometheus with Bearer Token

File: `claude-desktop-config-remote.json`

```json
{
  "mcpServers": {
    "prometheus-prod": {
      "command": "prometheus-mcp-server",
      "env": {
        "PROM_URL": "https://prometheus.prod.example.com",
        "PROM_TOKEN": "your_bearer_token_here",
        "PROM_TIMEOUT": "60"
      }
    }
  }
}
```

**Use case**: Production Prometheus with token authentication

### Basic Authentication

File: `claude-desktop-config-basicauth.json`

```json
{
  "mcpServers": {
    "prometheus": {
      "command": "prometheus-mcp-server",
      "env": {
        "PROM_URL": "https://prometheus.example.com",
        "PROM_USERNAME": "admin",
        "PROM_PASSWORD": "your_password_here"
      }
    }
  }
}
```

**Use case**: Prometheus behind HTTP basic auth

### Kubernetes In-Cluster

File: `claude-desktop-config-kubernetes.json`

```json
{
  "mcpServers": {
    "prometheus-k8s": {
      "command": "prometheus-mcp-server",
      "env": {
        "PROM_URL": "http://prometheus-server.monitoring.svc.cluster.local:9090"
      }
    }
  }
}
```

**Use case**: Accessing Prometheus running in Kubernetes cluster

### Using uvx (Recommended)

File: `claude-desktop-config-uvx.json`

```json
{
  "mcpServers": {
    "prometheus": {
      "command": "uvx",
      "args": ["prometheus-mcp-server"],
      "env": {
        "PROM_URL": "http://localhost:9090"
      }
    }
  }
}
```

**Use case**: Run without manual installation using uvx

## Configuration File Locations

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux
```
~/.config/Claude/claude_desktop_config.json
```

### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

## Example Queries

Once configured with Claude Desktop, try these queries:

### Basic Health Checks

```
"Is Prometheus healthy?"
"Show me all scrape targets"
"Which targets are down?"
```

### Metrics Exploration

```
"What metrics are available?"
"List all HTTP-related metrics"
"Show me the metadata for http_requests_total"
```

### Query Data

```
"What's the current CPU usage?"
"Show me the request rate for the API service over the last hour"
"What are the top 5 endpoints by request count?"
```

### Alert Investigation

```
"Show me all active alerts"
"Why is the HighMemoryUsage alert firing?"
"List all alerting rules"
```

### Troubleshooting

```
"Check the health of all targets in the 'api' job"
"Show me error rates for the last 6 hours"
"What's the cardinality of my metrics?"
```

## Testing Endpoints Manually

### Using curl

```bash
# Query instant
curl -G http://localhost:9090/api/v1/query \
  --data-urlencode 'query=up'

# Query range
curl -G http://localhost:9090/api/v1/query_range \
  --data-urlencode 'query=rate(http_requests_total[5m])' \
  --data-urlencode 'start=2024-01-15T00:00:00Z' \
  --data-urlencode 'end=2024-01-15T01:00:00Z' \
  --data-urlencode 'step=30s'

# List metrics
curl http://localhost:9090/api/v1/label/__name__/values

# List targets
curl http://localhost:9090/api/v1/targets

# List alerts
curl http://localhost:9090/api/v1/alerts
```

### Using Python

```python
import httpx

client = httpx.Client(base_url="http://localhost:9090")

# Query instant
response = client.get("/api/v1/query", params={"query": "up"})
print(response.json())

# List metrics
response = client.get("/api/v1/label/__name__/values")
print(response.json())

client.close()
```

## Troubleshooting

### Prometheus Not Starting

```bash
# Check logs
docker-compose logs prometheus

# Check configuration
docker exec prometheus-test promtool check config /etc/prometheus/prometheus.yml
```

### Connection Refused

```bash
# Verify Prometheus is running
docker ps | grep prometheus

# Check port binding
curl http://localhost:9090/-/healthy
```

### No Data in Prometheus

```bash
# Wait a minute for first scrape, then check targets
curl http://localhost:9090/api/v1/targets

# Check if metrics are being scraped
curl http://localhost:9090/api/v1/query?query=up
```

### Authentication Issues

```bash
# Test with token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:9090/api/v1/query?query=up

# Test with basic auth
curl -u username:password \
  http://localhost:9090/api/v1/query?query=up
```

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus API](https://prometheus.io/docs/prometheus/latest/querying/api/)
- [Node Exporter](https://github.com/prometheus/node_exporter)
- [cAdvisor](https://github.com/google/cadvisor)
