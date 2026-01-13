"""
Command-line interface for Prometheus MCP Server.

Provides a Click-based CLI for running the MCP server and testing
all Prometheus tools directly from the command line.
"""

import json
import sys
from collections.abc import Callable
from functools import wraps
from typing import Any

import click

from prometheus_mcp_server.server import create_server
from prometheus_mcp_server.utils.client import PrometheusClient
from prometheus_mcp_server.utils.helpers import parse_time


def common_options(func: Callable) -> Callable:
    """Decorator to add common Prometheus connection options."""

    @click.option(
        "--url",
        envvar=["PROM_URL", "PROMETHEUS_URL"],
        default="http://localhost:9090",
        help="Prometheus server URL (e.g., http://localhost:9090, https://prometheus.example.com).",
        show_envvar=True,
    )
    @click.option(
        "--token",
        envvar=["PROM_TOKEN", "PROMETHEUS_TOKEN"],
        default=None,
        help="Bearer token for authentication. Use for token-based auth.",
        show_envvar=True,
    )
    @click.option(
        "--username",
        envvar="PROM_USERNAME",
        default=None,
        help="Username for HTTP basic authentication.",
        show_envvar=True,
    )
    @click.option(
        "--password",
        envvar="PROM_PASSWORD",
        default=None,
        help="Password for HTTP basic authentication.",
        show_envvar=True,
    )
    @click.option(
        "--timeout",
        envvar="PROM_TIMEOUT",
        type=int,
        default=30,
        help="Request timeout in seconds. Increase for slow queries.",
        show_default=True,
    )
    @click.option(
        "--verify-ssl/--no-verify-ssl",
        envvar="PROM_VERIFY_SSL",
        default=True,
        help="Verify SSL certificates. Use --no-verify-ssl for self-signed certs.",
        show_default=True,
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_client(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> PrometheusClient:
    """Create a Prometheus client with the given options."""
    return PrometheusClient(
        url=url,
        token=token,
        username=username,
        password=password,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )


def output_response(response: Any, raw: bool = False) -> None:
    """Output response in formatted JSON."""
    if response.success:
        result = {"data": response.data}
        if response.warnings:
            result["warnings"] = response.warnings
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        click.echo(
            click.style(f"Error (HTTP {response.status_code}): {response.error}", fg="red"),
            err=True,
        )
        sys.exit(1)


# ============================================================
# Main CLI Group
# ============================================================


@click.group()
@click.version_option(package_name="prometheus-mcp-server")
def cli() -> None:
    """Prometheus MCP Server - Read-only metrics querying and monitoring.

    A Model Context Protocol (MCP) server that provides safe, read-only access
    to Prometheus monitoring platform. All operations are non-destructive.

    \b
    COMMAND GROUPS:
      run       Start the MCP server (stdio, HTTP, SSE transports)
      query     Execute PromQL instant and range queries
      metadata  Discover metrics, labels, and time series
      targets   Inspect scrape targets and their health
      alerts    View active alerts and alerting rules
      status    Check server health, config, and statistics
      promql    PromQL utilities (format, parse/validate)

    \b
    AUTHENTICATION:
      Set via options or environment variables:
        --url / PROM_URL           Prometheus server URL
        --token / PROM_TOKEN       Bearer token authentication
        --username / PROM_USERNAME Basic auth username
        --password / PROM_PASSWORD Basic auth password

    \b
    QUICK START:
      # Check connection
      prometheus-mcp-server check --url http://localhost:9090

      # Run instant query
      prometheus-mcp-server query instant "up"

      # Start MCP server
      prometheus-mcp-server run
    """
    pass


# ============================================================
# Server Commands
# ============================================================


@cli.command()
@common_options
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http", "sse", "streamable-http"]),
    default="stdio",
    help="MCP transport: stdio (CLI/pipes), http, sse, streamable-http.",
    show_default=True,
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Bind address for HTTP/SSE. Use 0.0.0.0 for all interfaces.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port for HTTP/SSE transport.",
    show_default=True,
)
def run(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    transport: str,
    host: str,
    port: int,
) -> None:
    """Run the Prometheus MCP server.

    Starts the MCP server that AI agents can connect to for querying Prometheus.
    The server provides 22 read-only tools for metrics, alerts, and status.

    \b
    TRANSPORTS:
      stdio           Standard I/O (default) - for CLI tools and local agents
      http            HTTP POST requests - for web-based integrations
      sse             Server-Sent Events - for real-time streaming
      streamable-http Streamable HTTP - for large responses

    \b
    EXAMPLES:
      # Run with stdio transport (default, for Claude Desktop)
      prometheus-mcp-server run

      # Run with HTTP transport on port 8000
      prometheus-mcp-server run --transport http --port 8000

      # Run with custom Prometheus URL and auth
      prometheus-mcp-server run --url https://prometheus.example.com --token $TOKEN

      # Run accessible from other hosts
      prometheus-mcp-server run --transport http --host 0.0.0.0 --port 8080
    """
    server = create_server(
        url=url,
        token=token,
        username=username,
        password=password,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )

    if transport == "stdio":
        server.run(transport="stdio")
    elif transport == "http":
        server.run(transport="http", host=host, port=port)
    elif transport == "sse":
        server.run(transport="sse", host=host, port=port)
    elif transport == "streamable-http":
        server.run(transport="streamable-http", host=host, port=port)


# ============================================================
# Query Commands Group
# ============================================================


@cli.group()
def query() -> None:
    """Execute PromQL queries against Prometheus.

    Run instant queries for current values or range queries for time-series data.

    \b
    COMMANDS:
      instant    Get current metric values at a point in time
      range      Get metric values over a time range (for graphing)
      exemplars  Get trace correlation data from histogram metrics

    \b
    TIME FORMATS (for --time, --start, --end):
      Relative:  now, now-1h, now-30m, now-1d, now-7d
      RFC3339:   2024-01-15T10:00:00Z
      Unix:      1705316400

    \b
    QUICK EXAMPLES:
      prometheus-mcp-server query instant "up"
      prometheus-mcp-server query range "rate(http_requests_total[5m])" -s now-1h -e now
    """
    pass


@query.command("instant")
@common_options
@click.argument("promql")
@click.option(
    "--time", "-t",
    default=None,
    help="Evaluation timestamp. Relative: now, now-1h. Absolute: RFC3339 or Unix timestamp.",
)
@click.option(
    "--query-timeout",
    default=None,
    help="Query timeout (e.g., 30s, 1m). Increase for complex queries.",
)
def query_instant(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    promql: str,
    time: str | None,
    query_timeout: str | None,
) -> None:
    """Execute a PromQL instant query at a single point in time.

    PROMQL is the PromQL expression to evaluate. Returns current metric values.

    \b
    PROMQL EXAMPLES:
      "up"                                    Check target health (1=up, 0=down)
      "up{job='api-server'}"                  Filter by label
      "rate(http_requests_total[5m])"         Per-second request rate
      "sum(rate(http_requests_total[5m])) by (status)"  Aggregated by status
      "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))"

    \b
    EXAMPLES:
      # Check which targets are up
      prometheus-mcp-server query instant "up"

      # Filter by job label
      prometheus-mcp-server query instant 'up{job="api-server"}'

      # Query at 1 hour ago
      prometheus-mcp-server query instant "up" -t now-1h

      # Calculate error rate percentage
      prometheus-mcp-server query instant \\
        'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'
    """
    params: dict[str, Any] = {"query": promql}

    if time:
        parsed_time = parse_time(time)
        if parsed_time:
            params["time"] = parsed_time

    if query_timeout:
        params["timeout"] = query_timeout

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/query", params=params)
        output_response(response)


@query.command("range")
@common_options
@click.argument("promql")
@click.option(
    "--start", "-s",
    required=True,
    help="Start of time range. Relative: now-1h, now-6h, now-1d. Or RFC3339/Unix.",
)
@click.option(
    "--end", "-e",
    required=True,
    help="End of time range. Usually 'now' for current data. Or RFC3339/Unix.",
)
@click.option(
    "--step",
    default="15s",
    help="Resolution step (time between points). 15s=high, 1m=medium, 5m=low resolution.",
    show_default=True,
)
@click.option(
    "--query-timeout",
    default=None,
    help="Query timeout (e.g., 1m, 5m). Increase for long ranges.",
)
def query_range(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    promql: str,
    start: str,
    end: str,
    step: str,
    query_timeout: str | None,
) -> None:
    """Execute a PromQL range query over a time period.

    PROMQL is the PromQL expression. Returns time series data for graphing/trending.

    \b
    STEP GUIDANCE:
      15s   High resolution - short ranges (<1h), detailed analysis
      1m    Medium resolution - medium ranges (1-6h), dashboards
      5m    Lower resolution - long ranges (1d+), trends

    \b
    EXAMPLES:
      # Request rate over last hour with 30s resolution
      prometheus-mcp-server query range 'rate(http_requests_total[5m])' \\
          -s now-1h -e now --step 30s

      # CPU usage over last 6 hours
      prometheus-mcp-server query range \\
          'avg(rate(container_cpu_usage_seconds_total[5m])) by (container)' \\
          -s now-6h -e now --step 1m

      # Error rate trend over last day
      prometheus-mcp-server query range \\
          'sum(rate(http_requests_total{status=~"5.."}[5m]))/sum(rate(http_requests_total[5m]))' \\
          -s now-1d -e now --step 5m

      # P99 latency over last week
      prometheus-mcp-server query range \\
          'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))' \\
          -s now-7d -e now --step 15m
    """
    params: dict[str, Any] = {
        "query": promql,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
        "step": step,
    }

    if query_timeout:
        params["timeout"] = query_timeout

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/query_range", params=params)
        output_response(response)


@query.command("exemplars")
@common_options
@click.argument("promql")
@click.option(
    "--start", "-s",
    required=True,
    help="Start of time range. Relative: now-1h. Or RFC3339/Unix timestamp.",
)
@click.option(
    "--end", "-e",
    required=True,
    help="End of time range. Usually 'now'. Or RFC3339/Unix timestamp.",
)
def query_exemplars(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    promql: str,
    start: str,
    end: str,
) -> None:
    """Query exemplars for distributed tracing correlation.

    PROMQL is typically a histogram bucket metric. Exemplars contain trace IDs
    linking metrics to specific distributed traces. Requires Prometheus configured
    with exemplar storage.

    \b
    EXAMPLES:
      # Get exemplars for HTTP latency histogram
      prometheus-mcp-server query exemplars \\
          "http_request_duration_seconds_bucket" -s now-1h -e now

      # Get exemplars for specific service
      prometheus-mcp-server query exemplars \\
          'http_request_duration_seconds_bucket{service="api"}' -s now-30m -e now

      # Get gRPC latency exemplars
      prometheus-mcp-server query exemplars \\
          'grpc_server_handling_seconds_bucket{grpc_service="UserService"}' -s now-15m -e now
    """
    params = {
        "query": promql,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
    }

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/query_exemplars", params=params)
        output_response(response)


# ============================================================
# Metadata Commands Group
# ============================================================


@cli.group()
def metadata() -> None:
    """Discover metrics, labels, and time series.

    Explore what metrics exist, their types, and available label values.
    Essential for understanding what data is available before writing queries.

    \b
    COMMANDS:
      metrics       List all metric names (optionally filtered)
      metric-info   Get metric type, help text, and unit
      labels        List all label names
      label-values  Get all values for a specific label
      series        Find time series matching label selectors

    \b
    DISCOVERY WORKFLOW:
      1. List metrics:       metadata metrics
      2. Get metric info:    metadata metric-info -m http_requests_total
      3. Find label values:  metadata label-values job
      4. Find series:        metadata series -m '{job="api"}'

    \b
    QUICK EXAMPLES:
      prometheus-mcp-server metadata metrics --match '{job="api"}'
      prometheus-mcp-server metadata label-values namespace
    """
    pass


@metadata.command("metrics")
@common_options
@click.option(
    "--match", "-m",
    default=None,
    help="Series selector to filter. E.g., '{job=\"api\"}' or '{__name__=~\"http_.*\"}'.",
)
def list_metrics(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    match: str | None,
) -> None:
    """List all available metric names.

    Returns unique metric names. Without --match, returns ALL metrics (can be thousands).
    Use --match to filter by job, namespace, or metric name pattern.

    \b
    MATCH SELECTOR EXAMPLES:
      '{job="api-server"}'          Metrics from specific job
      '{namespace="production"}'    Metrics from namespace
      '{__name__=~"http_.*"}'       Metrics starting with http_
      '{__name__=~".*_total"}'      Counter metrics ending in _total

    \b
    EXAMPLES:
      # List all metrics (may return many results)
      prometheus-mcp-server metadata metrics

      # List metrics from specific job
      prometheus-mcp-server metadata metrics -m '{job="kubernetes-pods"}'

      # Find HTTP-related metrics
      prometheus-mcp-server metadata metrics -m '{__name__=~"http_.*"}'
    """
    params = {}
    if match:
        params["match[]"] = match

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get(
            "/api/v1/label/__name__/values",
            params=params if params else None,
        )
        output_response(response)


@metadata.command("metric-info")
@common_options
@click.option(
    "--metric", "-m",
    default=None,
    help="Specific metric name. Without this, returns ALL metrics' metadata.",
)
@click.option(
    "--limit", "-l",
    type=int,
    default=None,
    help="Maximum number of metrics to return. Useful when querying all.",
)
def get_metric_metadata(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    metric: str | None,
    limit: int | None,
) -> None:
    """Get metric type, help text, and unit information.

    Returns metadata that describes what metrics measure and how to interpret them.
    Includes: type (counter/gauge/histogram/summary), help (description), unit.

    \b
    METRIC TYPES:
      counter    Monotonically increasing (requests, errors). Use rate().
      gauge      Can go up/down (temperature, memory). Use directly.
      histogram  Distribution in buckets. Use histogram_quantile().
      summary    Pre-computed percentiles. Use directly.

    \b
    EXAMPLES:
      # Get metadata for specific metric
      prometheus-mcp-server metadata metric-info -m http_requests_total

      # Get metadata for process metrics
      prometheus-mcp-server metadata metric-info -m process_cpu_seconds_total

      # Get first 50 metrics' metadata
      prometheus-mcp-server metadata metric-info -l 50

      # Understand a histogram metric
      prometheus-mcp-server metadata metric-info -m http_request_duration_seconds
    """
    params = {}
    if metric:
        params["metric"] = metric
    if limit:
        params["limit"] = limit

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/metadata", params=params if params else None)
        output_response(response)


@metadata.command("labels")
@common_options
@click.option(
    "--match", "-m",
    multiple=True,
    help="Series selector to filter. Can be repeated for multiple selectors.",
)
@click.option("--start", "-s", default=None, help="Start timestamp to limit time range.")
@click.option("--end", "-e", default=None, help="End timestamp to limit time range.")
def list_labels(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    match: tuple[str, ...],
    start: str | None,
    end: str | None,
) -> None:
    """List all label names used across metrics.

    Returns unique label names (keys). Use this to discover what labels are available
    for filtering queries. Common labels: job, instance, namespace, pod, container.

    \b
    EXAMPLES:
      # List all labels in Prometheus
      prometheus-mcp-server metadata labels

      # List labels for a specific job
      prometheus-mcp-server metadata labels -m '{job="kubernetes-pods"}'

      # List labels for HTTP metrics
      prometheus-mcp-server metadata labels -m '{__name__=~"http_.*"}'

      # List labels with time filter
      prometheus-mcp-server metadata labels -m '{job="api"}' -s now-1h -e now
    """
    params: dict[str, Any] = {}
    if match:
        params["match[]"] = list(match)
    if start:
        params["start"] = parse_time(start)
    if end:
        params["end"] = parse_time(end)

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/labels", params=params if params else None)
        output_response(response)


@metadata.command("label-values")
@common_options
@click.argument("label")
@click.option(
    "--match", "-m",
    multiple=True,
    help="Series selector to filter scope. Can be repeated.",
)
@click.option("--start", "-s", default=None, help="Start timestamp to limit time range.")
@click.option("--end", "-e", default=None, help="End timestamp to limit time range.")
def get_label_values(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    label: str,
    match: tuple[str, ...],
    start: str | None,
    end: str | None,
) -> None:
    """Get all unique values for a specific label.

    LABEL is the label name to get values for (e.g., job, namespace, instance).
    Returns array of unique values. Use --match to filter scope.

    \b
    COMMON LABELS:
      job         Scrape job names
      instance    Target addresses (host:port)
      namespace   Kubernetes namespaces
      pod         Kubernetes pod names
      container   Container names
      service     Service names
      __name__    Metric names

    \b
    EXAMPLES:
      # Get all job names
      prometheus-mcp-server metadata label-values job

      # Get all namespaces
      prometheus-mcp-server metadata label-values namespace

      # Get instances for specific job
      prometheus-mcp-server metadata label-values instance -m '{job="api-server"}'

      # Get pods in production namespace
      prometheus-mcp-server metadata label-values pod -m '{namespace="production"}'

      # Get status codes from HTTP metrics
      prometheus-mcp-server metadata label-values status_code -m '{__name__=~"http_.*"}'
    """
    params: dict[str, Any] = {}
    if match:
        params["match[]"] = list(match)
    if start:
        params["start"] = parse_time(start)
    if end:
        params["end"] = parse_time(end)

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get(
            f"/api/v1/label/{label}/values",
            params=params if params else None,
        )
        output_response(response)


@metadata.command("series")
@common_options
@click.option(
    "--match", "-m",
    required=True,
    multiple=True,
    help="Series selector (required). Can repeat for multiple selectors (union).",
)
@click.option("--start", "-s", default=None, help="Start timestamp to limit time range.")
@click.option("--end", "-e", default=None, help="End timestamp to limit time range.")
def find_series(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    match: tuple[str, ...],
    start: str | None,
    end: str | None,
) -> None:
    """Find all time series matching label selectors.

    Returns the full label set for each matching series. Unlike 'metrics' which
    returns only names, this shows all labels for each series. Useful for
    understanding cardinality and finding specific series.

    \b
    MATCH SELECTOR SYNTAX:
      {job="api"}                   Exact match
      {job=~"api-.*"}               Regex match
      {namespace!="kube-system"}    Not equal
      {job="a",namespace="prod"}    Multiple conditions (AND)

    \b
    EXAMPLES:
      # Find all series for a job
      prometheus-mcp-server metadata series -m '{job="api-server"}'

      # Find all 'up' metric series (to see targets)
      prometheus-mcp-server metadata series -m '{__name__="up"}'

      # Find HTTP metrics in production
      prometheus-mcp-server metadata series -m '{__name__=~"http_.*",namespace="production"}'

      # Find series with time filter
      prometheus-mcp-server metadata series -m '{job="api"}' -s now-1h -e now

      # Find series from multiple jobs (union)
      prometheus-mcp-server metadata series -m '{job="frontend"}' -m '{job="backend"}'
    """
    params: dict[str, Any] = {"match[]": list(match)}
    if start:
        params["start"] = parse_time(start)
    if end:
        params["end"] = parse_time(end)

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.post("/api/v1/series", data=params)
        output_response(response)


# ============================================================
# Targets Commands Group
# ============================================================


@cli.group()
def targets() -> None:
    """Inspect Prometheus scrape targets and their health.

    View what endpoints Prometheus is scraping, their health status, and metadata
    about metrics they expose. Essential for debugging scraping issues.

    \b
    COMMANDS:
      list      Show all scrape targets with health status
      metadata  Get metric metadata reported by targets

    \b
    EXAMPLES:
      prometheus-mcp-server targets list --state active
      prometheus-mcp-server targets metadata --match-target '{job="api"}'
    """
    pass


@targets.command("list")
@common_options
@click.option(
    "--state",
    type=click.Choice(["any", "active", "dropped"]),
    default="any",
    help="Filter by state: any (all), active (being scraped), dropped (filtered out).",
    show_default=True,
)
def list_targets(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    state: str,
) -> None:
    """List all scrape targets and their current health status.

    Shows discovered targets, their labels, health (up/down), last scrape time,
    and any errors. Use to verify scraping is working correctly.

    \b
    TARGET STATES:
      active   Currently being scraped (healthy or unhealthy)
      dropped  Filtered out by relabeling rules (not scraped)
      any      Both active and dropped

    \b
    OUTPUT INCLUDES:
      - labels: Target identifying labels (job, instance, etc.)
      - scrapeUrl: Full URL being scraped
      - health: "up" (successful) or "down" (failed)
      - lastScrape: When last scraped
      - lastError: Error message if scrape failed

    \b
    EXAMPLES:
      # List all targets
      prometheus-mcp-server targets list

      # List only active/healthy targets
      prometheus-mcp-server targets list --state active

      # List dropped targets (to debug relabeling)
      prometheus-mcp-server targets list --state dropped
    """
    params = {"state": state}

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/targets", params=params)
        output_response(response)


@targets.command("metadata")
@common_options
@click.option(
    "--match-target", "-m",
    default=None,
    help="Label selector to filter targets. E.g., '{job=\"api\"}'.",
)
@click.option(
    "--metric",
    default=None,
    help="Filter by specific metric name.",
)
@click.option(
    "--limit", "-l",
    type=int,
    default=None,
    help="Maximum number of results to return.",
)
def get_targets_metadata(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    match_target: str | None,
    metric: str | None,
    limit: int | None,
) -> None:
    """Get metric metadata reported by scrape targets.

    Returns metadata (type, help text, unit) for metrics as reported by the targets
    themselves in their /metrics endpoint. Different from 'metadata metric-info'
    which shows aggregated metadata.

    \b
    EXAMPLES:
      # Get all metadata from api-server targets
      prometheus-mcp-server targets metadata -m '{job="api-server"}'

      # Get metadata for specific metric across all targets
      prometheus-mcp-server targets metadata --metric http_requests_total

      # Get metadata for metric from specific job
      prometheus-mcp-server targets metadata \\
          -m '{job="node-exporter"}' --metric node_cpu_seconds_total

      # Limit results
      prometheus-mcp-server targets metadata -l 100
    """
    params = {}
    if match_target:
        params["match_target"] = match_target
    if metric:
        params["metric"] = metric
    if limit:
        params["limit"] = limit

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get(
            "/api/v1/targets/metadata",
            params=params if params else None,
        )
        output_response(response)


# ============================================================
# Alerts Commands Group
# ============================================================


@cli.group()
def alerts() -> None:
    """View active alerts and configured alerting/recording rules.

    Check what alerts are currently firing or pending, and inspect the rules
    that define how alerts are generated.

    \b
    COMMANDS:
      list   Show currently active alerts (firing + pending)
      rules  Show all configured alerting and recording rules

    \b
    ALERT STATES:
      firing    Alert condition met for required duration
      pending   Alert condition met but not yet for full duration

    \b
    EXAMPLES:
      prometheus-mcp-server alerts list
      prometheus-mcp-server alerts rules --type alert
    """
    pass


@alerts.command("list")
@common_options
def list_alerts(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """List all currently active alerts (firing and pending).

    Shows alerts that are currently active - either firing (condition met for
    required duration) or pending (condition met but waiting for duration).

    \b
    OUTPUT INCLUDES:
      - labels: Alert identity (alertname, severity, etc.)
      - annotations: Descriptions (summary, description, runbook_url)
      - state: "firing" or "pending"
      - activeAt: When the alert became active
      - value: Current metric value triggering the alert

    \b
    EXAMPLES:
      # List all active alerts
      prometheus-mcp-server alerts list

    Use 'alerts rules --type alert' to see all configured alert definitions.
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/alerts")
        output_response(response)


@alerts.command("rules")
@common_options
@click.option(
    "--type", "rule_type",
    type=click.Choice(["alert", "record"]),
    default=None,
    help="Filter by type: alert (alerting rules) or record (recording rules).",
)
def list_rules(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    rule_type: str | None,
) -> None:
    """List all configured recording and alerting rules.

    Shows rule definitions grouped by file and rule group. Includes current
    evaluation status and any errors.

    \b
    RULE TYPES:
      alert   Rules that fire alerts when conditions are met
      record  Rules that precompute expressions into new metrics

    \b
    OUTPUT INCLUDES:
      - groups: Rule groups with name, file, interval
      - rules: Individual rules with query, labels, annotations
      - health: Rule evaluation health status
      - lastError: Any evaluation errors

    \b
    EXAMPLES:
      # List all rules
      prometheus-mcp-server alerts rules

      # List only alerting rules
      prometheus-mcp-server alerts rules --type alert

      # List only recording rules
      prometheus-mcp-server alerts rules --type record
    """
    params = {}
    if rule_type:
        params["type"] = rule_type

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/rules", params=params if params else None)
        output_response(response)


# ============================================================
# Status Commands Group
# ============================================================


@cli.group()
def status() -> None:
    """Check Prometheus server health, configuration, and statistics.

    Inspect server health, readiness, configuration, and storage statistics.
    Essential for operational monitoring and troubleshooting.

    \b
    COMMANDS:
      health     Basic liveness check (is server running?)
      ready      Readiness check (can server handle queries?)
      buildinfo  Version and build information
      config     Currently loaded YAML configuration
      flags      Runtime flags and settings
      runtime    Runtime info (uptime, goroutines, etc.)
      tsdb       TSDB cardinality and storage statistics
      walreplay  WAL replay progress (after restart)

    \b
    COMMON WORKFLOW:
      1. Check health:    status health
      2. Check readiness: status ready
      3. Get version:     status buildinfo
      4. Debug storage:   status tsdb

    \b
    EXAMPLES:
      prometheus-mcp-server status health
      prometheus-mcp-server status tsdb
    """
    pass


@status.command("health")
@common_options
def check_health(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Check if Prometheus server is healthy (liveness check).

    Basic health check - returns healthy if Prometheus is running and responding.
    Use for liveness probes. For query readiness, use 'status ready' instead.

    \b
    EXAMPLES:
      prometheus-mcp-server status health
      prometheus-mcp-server status health --url https://prometheus.example.com
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/-/healthy")
        if response.status_code == 200:
            click.echo(json.dumps({"status": "healthy"}, indent=2))
        else:
            click.echo(json.dumps({"status": "unhealthy", "error": response.error}, indent=2))
            sys.exit(1)


@status.command("ready")
@common_options
def check_readiness(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Check if Prometheus is ready to serve queries (readiness check).

    Readiness check - returns ready when Prometheus has completed startup
    (including WAL replay) and can serve accurate query results. Use for
    readiness probes. Check after restart before sending queries.

    \b
    EXAMPLES:
      prometheus-mcp-server status ready
      prometheus-mcp-server status ready --url https://prometheus.example.com
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/-/ready")
        if response.status_code == 200:
            click.echo(json.dumps({"status": "ready"}, indent=2))
        else:
            click.echo(json.dumps({"status": "not_ready", "error": response.error}, indent=2))
            sys.exit(1)


@status.command("config")
@common_options
def get_config(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get the currently loaded Prometheus configuration.

    Returns the full YAML configuration that was loaded at startup. Includes
    global settings, scrape_configs, alerting rules, remote_write/read, etc.
    Sensitive values may be redacted.

    \b
    EXAMPLES:
      prometheus-mcp-server status config
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/status/config")
        output_response(response)


@status.command("flags")
@common_options
def get_flags(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get Prometheus command-line flags and their values.

    Returns all startup flags showing how Prometheus was configured at launch.
    Includes storage paths, retention, web settings, and feature flags.

    \b
    COMMON FLAGS:
      storage.tsdb.path            Data storage directory
      storage.tsdb.retention.time  Data retention period
      web.listen-address           HTTP server address
      web.enable-lifecycle         If lifecycle endpoints enabled
      web.enable-admin-api         If admin API enabled

    \b
    EXAMPLES:
      prometheus-mcp-server status flags
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/status/flags")
        output_response(response)


@status.command("runtime")
@common_options
def get_runtime_info(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get Prometheus server runtime information.

    Returns detailed runtime info including version, uptime, memory usage,
    goroutine count, and storage retention settings.

    \b
    OUTPUT INCLUDES:
      - startTime: When Prometheus started
      - reloadConfigSuccess: If last config reload succeeded
      - lastConfigTime: When config was last reloaded
      - goroutineCount: Number of goroutines
      - storageRetention: Data retention period
      - GOMAXPROCS, GOGC: Go runtime settings

    \b
    EXAMPLES:
      prometheus-mcp-server status runtime
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/status/runtimeinfo")
        output_response(response)


@status.command("tsdb")
@common_options
def get_tsdb_stats(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get TSDB cardinality and storage statistics.

    Returns storage statistics useful for capacity planning and debugging
    high-cardinality issues. Shows top metrics by series count, labels
    with most unique values, and memory usage.

    \b
    OUTPUT INCLUDES:
      - headStats: Series count, chunks, samples in head block
      - seriesCountByMetricName: Top metrics by cardinality
      - labelValueCountByLabelName: Labels with most unique values
      - memoryInBytesByLabelName: Memory usage per label
      - seriesCountByLabelValuePair: Top label-value pairs

    \b
    USE CASES:
      - Identify high-cardinality metrics causing storage bloat
      - Find labels with too many unique values
      - Plan storage capacity

    \b
    EXAMPLES:
      prometheus-mcp-server status tsdb
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/status/tsdb")
        output_response(response)


@status.command("buildinfo")
@common_options
def get_build_info(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get Prometheus version and build information.

    Returns version, Git revision, build date, and Go version. Useful for
    identifying the exact Prometheus version running.

    \b
    OUTPUT INCLUDES:
      - version: Prometheus version (e.g., "2.47.0")
      - revision: Git commit hash
      - branch: Git branch name
      - buildUser: Who built this binary
      - buildDate: When it was built
      - goVersion: Go compiler version

    \b
    EXAMPLES:
      prometheus-mcp-server status buildinfo
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/status/buildinfo")
        output_response(response)


@status.command("walreplay")
@common_options
def get_wal_replay_status(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get WAL (Write-Ahead Log) replay progress.

    Check WAL replay status after Prometheus restarts. WAL replay restores
    in-memory data from the write-ahead log, which can take time for large
    datasets. Once complete, min ≈ max ≈ current.

    \b
    OUTPUT INCLUDES:
      - min: First WAL segment to replay
      - max: Last WAL segment to replay
      - current: Currently replaying segment
      - state: Current replay state

    \b
    EXAMPLES:
      prometheus-mcp-server status walreplay
    """
    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/status/walreplay")
        output_response(response)


# ============================================================
# Query Utility Commands Group
# ============================================================


@cli.group("promql")
def promql() -> None:
    """PromQL query utilities for formatting and validation.

    Tools to format, prettify, and validate PromQL expressions without
    executing them. Useful for query development and debugging.

    \b
    COMMANDS:
      format  Format/prettify a PromQL query with consistent style
      parse   Parse and validate query syntax, return AST

    \b
    EXAMPLES:
      prometheus-mcp-server promql format 'sum(rate(x[5m]))by(job)'
      prometheus-mcp-server promql parse 'rate(http_requests_total[5m])'
    """
    pass


@promql.command("format")
@common_options
@click.argument("query")
def format_query(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    query: str,
) -> None:
    """Format and prettify a PromQL query expression.

    QUERY is the PromQL expression to format. Prometheus parses and re-serializes
    the query with consistent spacing and structure.

    \b
    EXAMPLES:
      # Format compact query
      prometheus-mcp-server promql format 'sum(rate(http_requests_total[5m]))by(status)'
      # Returns: "sum by (status) (rate(http_requests_total[5m]))"

      # Format query with inconsistent spacing
      prometheus-mcp-server promql format 'rate(  http_requests_total{job="api"}[5m])'

      # Format complex histogram query
      prometheus-mcp-server promql format 'histogram_quantile(0.99,sum(rate(x_bucket[5m]))by(le))'
    """
    params = {"query": query}

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/format_query", params=params)
        output_response(response)


@promql.command("parse")
@common_options
@click.argument("query")
def parse_query(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
    query: str,
) -> None:
    """Parse a PromQL query and return its AST (Abstract Syntax Tree).

    QUERY is the PromQL expression to parse. Validates syntax without executing.
    Returns the parsed structure for valid queries, or error message with
    position for invalid queries.

    \b
    USE CASES:
      - Validate query syntax before execution
      - Understand how Prometheus interprets a query
      - Debug complex query structures

    \b
    EXAMPLES:
      # Parse a simple metric
      prometheus-mcp-server promql parse 'up'

      # Parse a rate function
      prometheus-mcp-server promql parse 'rate(http_requests_total[5m])'

      # Validate complex query
      prometheus-mcp-server promql parse 'histogram_quantile(0.99, sum(rate(x_bucket[5m])) by (le))'

      # Test invalid query (will show parse error)
      prometheus-mcp-server promql parse 'rate(http_requests_total[5m]'
    """
    params = {"query": query}

    with get_client(url, token, username, password, timeout, verify_ssl) as client:
        response = client.get("/api/v1/parse_query", params=params)
        output_response(response)


# ============================================================
# Utility Commands
# ============================================================


@cli.command()
@common_options
def check(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Check connection to Prometheus server.

    Verifies connectivity, authentication, and retrieves version info.
    Use this before starting the MCP server to validate settings.

    \b
    CHECKS PERFORMED:
      - Health endpoint (/-/healthy)
      - Readiness endpoint (/-/ready)
      - Runtime info (version)

    \b
    EXAMPLES:
      # Check default localhost
      prometheus-mcp-server check

      # Check remote server
      prometheus-mcp-server check --url https://prometheus.example.com

      # Check with authentication
      prometheus-mcp-server check --url https://prometheus.example.com --token $TOKEN
    """
    click.echo(f"Checking connection to {url}...")

    client = get_client(url, token, username, password, timeout, verify_ssl)

    try:
        # Check health endpoint
        response = client.get("/-/healthy")
        if response.status_code == 200:
            click.echo(click.style("  Health check: OK", fg="green"))
        else:
            click.echo(click.style(f"  Health check: FAILED ({response.error})", fg="red"))

        # Check readiness endpoint
        response = client.get("/-/ready")
        if response.status_code == 200:
            click.echo(click.style("  Readiness check: OK", fg="green"))
        else:
            click.echo(click.style(f"  Readiness check: FAILED ({response.error})", fg="red"))

        # Get build info for version
        response = client.get("/api/v1/status/buildinfo")
        if response.success and response.data:
            version = response.data.get("version", "unknown")
            click.echo(f"  Prometheus version: {version}")
            click.echo(click.style("\nConnection successful!", fg="green", bold=True))
        else:
            click.echo(click.style(f"  Failed to get build info: {response.error}", fg="yellow"))

    except Exception as e:
        click.echo(click.style(f"\nConnection failed: {e}", fg="red", bold=True))
        sys.exit(1)
    finally:
        client.close()


@cli.command()
def info() -> None:
    """Display available MCP tools and their CLI command equivalents.

    Shows the complete mapping between MCP tools (used by AI agents) and CLI
    commands (for manual testing). All 22 tools are read-only and safe.
    """
    click.echo("Prometheus MCP Server - Tools & CLI Commands\n")
    click.echo("=" * 60)

    mappings = [
        ("Query Tools", [
            ("query_instant", "query instant", "Instant PromQL query"),
            ("query_range", "query range", "Range PromQL query"),
            ("query_exemplars", "query exemplars", "Query exemplars"),
        ]),
        ("Metadata Discovery", [
            ("list_metrics", "metadata metrics", "List metric names"),
            ("get_metric_metadata", "metadata metric-info", "Get metric metadata"),
            ("list_labels", "metadata labels", "List label names"),
            ("get_label_values", "metadata label-values", "Get label values"),
            ("find_series", "metadata series", "Find time series"),
        ]),
        ("Target & Scrape", [
            ("list_targets", "targets list", "List scrape targets"),
            ("get_targets_metadata", "targets metadata", "Get target metadata"),
        ]),
        ("Alerting", [
            ("list_alerts", "alerts list", "List active alerts"),
            ("list_rules", "alerts rules", "List rules"),
        ]),
        ("Status", [
            ("get_config", "status config", "Get configuration"),
            ("get_flags", "status flags", "Get runtime flags"),
            ("get_runtime_info", "status runtime", "Get runtime info"),
            ("get_tsdb_stats", "status tsdb", "Get TSDB stats"),
            ("get_build_info", "status buildinfo", "Get build info"),
            ("get_wal_replay_status", "status walreplay", "Get WAL replay status"),
            ("check_health", "status health", "Check health"),
            ("check_readiness", "status ready", "Check readiness"),
        ]),
        ("PromQL Utilities", [
            ("format_query", "promql format", "Format PromQL query"),
            ("parse_query", "promql parse", "Parse/validate query"),
        ]),
    ]

    for category, tool_list in mappings:
        click.echo(f"\n{click.style(category, bold=True)}")
        click.echo("-" * len(category))
        click.echo(f"  {'MCP Tool':<25} {'CLI Command':<25} Description")
        click.echo(f"  {'-'*24} {'-'*24} {'-'*20}")
        for mcp_tool, cli_cmd, description in tool_list:
            click.echo(
                f"  {click.style(mcp_tool, fg='cyan'):<34} "
                f"{click.style(cli_cmd, fg='yellow'):<34} "
                f"{description}"
            )

    click.echo("\n" + "=" * 60)
    click.echo("All operations are READ-ONLY and safe to use.")
    click.echo("\nRun 'prometheus-mcp-server <command> --help' for details.")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
