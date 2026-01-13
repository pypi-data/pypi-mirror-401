"""
Prometheus MCP Server.

A read-only MCP server for Prometheus monitoring platform.
All operations are safe and cannot modify Prometheus configuration.
"""

from mcp.server.fastmcp import FastMCP

from prometheus_mcp_server.tools.registry import PrometheusTools

SERVER_INSTRUCTIONS = """
Prometheus MCP Server - Read-Only Metrics & Monitoring

This server provides read-only access to Prometheus monitoring platform.
All operations are safe and cannot modify your Prometheus configuration.

## Available Tools:

### Query Tools
- **query_instant**: Execute PromQL instant query at a single point in time
- **query_range**: Execute PromQL query over a time range
- **query_exemplars**: Query exemplars for tracing correlation

### Metadata Discovery
- **list_metrics**: List all available metrics
- **get_metric_metadata**: Get metadata (type, help text) for metrics
- **list_labels**: List all label names
- **get_label_values**: Get all values for a specific label
- **find_series**: Find time series matching label selectors

### Target & Scrape Discovery
- **list_targets**: List all scrape targets and their status
- **get_targets_metadata**: Get metadata about metrics from targets

### Alerting
- **list_alerts**: List all active alerts (firing and pending)
- **list_rules**: List all recording and alerting rules

### Configuration & Status
- **get_config**: Get Prometheus configuration
- **get_flags**: Get runtime flags
- **get_runtime_info**: Get version and runtime information
- **get_tsdb_stats**: Get TSDB statistics and cardinality
- **check_health**: Check Prometheus health status
- **check_readiness**: Check if Prometheus is ready to serve queries

## PromQL Query Examples:

### Basic Queries:
```
up                                    # Check which targets are up
up{job="api-server"}                  # Filter by label
http_requests_total                   # Total HTTP requests
```

### Rate Queries:
```
rate(http_requests_total[5m])                      # Request rate
sum(rate(http_requests_total[5m])) by (status)     # Rate by status
irate(cpu_seconds_total[1m])                       # Instant rate
```

### Aggregation:
```
avg(cpu_usage) by (instance)                       # Average by instance
sum(memory_usage) by (namespace)                   # Sum by namespace
max(response_time) by (endpoint)                   # Max by endpoint
count(up) by (job)                                 # Count by job
```

### Advanced Queries:
```
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
predict_linear(disk_usage[1h], 3600)
delta(cpu_temp[5m])
```

## Time Formats:

Supported time formats:
- RFC3339: "2024-01-15T10:00:00Z"
- Unix timestamp: "1705316400"
- Relative: "now", "now-1h", "now-6h", "now-1d"

## Authentication:

Set environment variables:
- PROM_URL or PROMETHEUS_URL: Prometheus server URL
- PROM_TOKEN or PROMETHEUS_TOKEN: Bearer token (optional)
- PROM_USERNAME: Username for basic auth (optional)
- PROM_PASSWORD: Password for basic auth (optional)

## Safety:
- All operations are READ-ONLY
- Write operations are blocked
- Only query and metadata operations allowed
"""


def create_server(
    url: str | None = None,
    token: str | None = None,
    username: str | None = None,
    password: str | None = None,
    timeout: int = 30,
    verify_ssl: bool = True,
) -> FastMCP:
    """
    Create and configure the Prometheus MCP server.

    Args:
        url: Prometheus server URL
        token: Bearer token for authentication (optional)
        username: Username for basic auth (optional)
        password: Password for basic auth (optional)
        timeout: Request timeout in seconds
        verify_ssl: Verify SSL certificates

    Returns:
        Configured FastMCP server instance
    """
    mcp = FastMCP(
        name="prometheus-mcp-server",
        instructions=SERVER_INSTRUCTIONS,
    )

    # Register all Prometheus tools
    PrometheusTools(
        mcp=mcp,
        url=url,
        token=token,
        username=username,
        password=password,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )

    return mcp


def main() -> None:
    """Entry point for the Prometheus MCP server."""
    from prometheus_mcp_server.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
