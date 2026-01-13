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
        help="Prometheus server URL.",
        show_envvar=True,
    )
    @click.option(
        "--token",
        envvar=["PROM_TOKEN", "PROMETHEUS_TOKEN"],
        default=None,
        help="Bearer token for authentication.",
        show_envvar=True,
    )
    @click.option(
        "--username",
        envvar="PROM_USERNAME",
        default=None,
        help="Username for basic auth.",
        show_envvar=True,
    )
    @click.option(
        "--password",
        envvar="PROM_PASSWORD",
        default=None,
        help="Password for basic auth.",
        show_envvar=True,
    )
    @click.option(
        "--timeout",
        envvar="PROM_TIMEOUT",
        type=int,
        default=30,
        help="Request timeout in seconds.",
        show_default=True,
    )
    @click.option(
        "--verify-ssl/--no-verify-ssl",
        envvar="PROM_VERIFY_SSL",
        default=True,
        help="Verify SSL certificates.",
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

    A Model Context Protocol (MCP) server that provides read-only access
    to Prometheus monitoring platform.

    \b
    Commands are organized into groups:
      run       Start the MCP server
      query     Execute PromQL queries
      metadata  Discover metrics and labels
      targets   Inspect scrape targets
      alerts    View alerts and rules
      status    Check server status and configuration
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
    help="Transport mechanism for MCP communication.",
    show_default=True,
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host for HTTP/SSE transport.",
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

    \b
    Examples:
      # Run with stdio transport (default)
      prometheus-mcp-server run

      # Run with HTTP transport
      prometheus-mcp-server run --transport http --port 8000

      # Run with custom Prometheus URL
      prometheus-mcp-server run --url https://prometheus.example.com
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
    """Execute PromQL queries.

    \b
    Available commands:
      instant    Execute instant query at a single point in time
      range      Execute range query over a time period
      exemplars  Query exemplars for tracing correlation
    """
    pass


@query.command("instant")
@common_options
@click.argument("promql")
@click.option(
    "--time", "-t",
    default=None,
    help="Evaluation timestamp (RFC3339, Unix, or 'now', 'now-1h').",
)
@click.option(
    "--query-timeout",
    default=None,
    help="Query evaluation timeout (e.g., '30s', '1m').",
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
    """Execute a PromQL instant query.

    \b
    Examples:
      # Check which targets are up
      prometheus-mcp-server query instant "up"

      # Query with label filter
      prometheus-mcp-server query instant 'up{job="api-server"}'

      # Query at specific time
      prometheus-mcp-server query instant "up" --time "now-1h"

      # Request rate over last 5 minutes
      prometheus-mcp-server query instant 'rate(http_requests_total[5m])'
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
    help="Start timestamp (RFC3339, Unix, or 'now-6h').",
)
@click.option(
    "--end", "-e",
    required=True,
    help="End timestamp (RFC3339, Unix, or 'now').",
)
@click.option(
    "--step",
    default="15s",
    help="Query resolution step (e.g., '15s', '1m', '5m').",
    show_default=True,
)
@click.option(
    "--query-timeout",
    default=None,
    help="Query evaluation timeout.",
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

    \b
    Examples:
      # Request rate over last hour
      prometheus-mcp-server query range 'rate(http_requests_total[5m])' \\
          --start now-1h --end now

      # CPU usage with 1-minute resolution
      prometheus-mcp-server query range 'avg(cpu_usage) by (instance)' \\
          --start now-6h --end now --step 1m
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
    help="Start timestamp.",
)
@click.option(
    "--end", "-e",
    required=True,
    help="End timestamp.",
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
    """Query exemplars for tracing correlation.

    Exemplars link metrics to traces via trace IDs.

    \b
    Examples:
      prometheus-mcp-server query exemplars \\
          "http_request_duration_seconds_bucket" \\
          --start now-1h --end now
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
    """Discover metrics, labels, and series.

    \b
    Available commands:
      metrics         List all metric names
      metric-info     Get metadata for a metric
      labels          List all label names
      label-values    Get values for a label
      series          Find matching time series
    """
    pass


@metadata.command("metrics")
@common_options
@click.option(
    "--match", "-m",
    default=None,
    help="Metric name filter (regex pattern).",
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

    \b
    Examples:
      # List all metrics
      prometheus-mcp-server metadata metrics

      # Filter by pattern
      prometheus-mcp-server metadata metrics --match "http_.*"
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
    help="Specific metric name (returns all if not specified).",
)
@click.option(
    "--limit", "-l",
    type=int,
    default=None,
    help="Maximum number of metrics to return.",
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
    """Get metadata (type, help text) for metrics.

    \b
    Examples:
      # Get all metric metadata
      prometheus-mcp-server metadata metric-info

      # Get metadata for specific metric
      prometheus-mcp-server metadata metric-info --metric http_requests_total
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
    help="Label matcher to filter (can be repeated).",
)
@click.option("--start", "-s", default=None, help="Start timestamp.")
@click.option("--end", "-e", default=None, help="End timestamp.")
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
    """List all label names.

    \b
    Examples:
      # List all labels
      prometheus-mcp-server metadata labels

      # Filter by matcher
      prometheus-mcp-server metadata labels --match '{job="api"}'
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
    help="Label matcher to filter (can be repeated).",
)
@click.option("--start", "-s", default=None, help="Start timestamp.")
@click.option("--end", "-e", default=None, help="End timestamp.")
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
    """Get all values for a specific label.

    \b
    Examples:
      # Get all job names
      prometheus-mcp-server metadata label-values job

      # Get namespaces for production cluster
      prometheus-mcp-server metadata label-values namespace \\
          --match '{cluster="prod"}'
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
    help="Series selector (required, can be repeated).",
)
@click.option("--start", "-s", default=None, help="Start timestamp.")
@click.option("--end", "-e", default=None, help="End timestamp.")
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
    """Find time series matching label selectors.

    \b
    Examples:
      # Find all series for a job
      prometheus-mcp-server metadata series --match '{job="api"}'

      # Find HTTP metrics
      prometheus-mcp-server metadata series --match '{__name__=~"http_.*"}'
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
    """Inspect scrape targets and their metadata.

    \b
    Available commands:
      list      List all scrape targets
      metadata  Get metadata from targets
    """
    pass


@targets.command("list")
@common_options
@click.option(
    "--state",
    type=click.Choice(["any", "active", "dropped"]),
    default="any",
    help="Filter by target state.",
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
    """List all scrape targets and their status.

    \b
    Examples:
      # List all targets
      prometheus-mcp-server targets list

      # List only active targets
      prometheus-mcp-server targets list --state active

      # List dropped targets
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
    help="Label selector to filter targets.",
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
    help="Maximum results to return.",
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
    """Get metadata about metrics scraped from targets.

    \b
    Examples:
      # Get all target metadata
      prometheus-mcp-server targets metadata

      # Filter by target
      prometheus-mcp-server targets metadata --match-target '{job="api"}'

      # Filter by metric
      prometheus-mcp-server targets metadata --metric http_requests_total
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
    """View alerts and alerting/recording rules.

    \b
    Available commands:
      list   List all active alerts
      rules  List alerting and recording rules
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
    """List all active alerts (firing and pending).

    \b
    Examples:
      prometheus-mcp-server alerts list
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
    help="Filter by rule type.",
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
    """List all recording and alerting rules.

    \b
    Examples:
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
    """Check server status and configuration.

    \b
    Available commands:
      health     Check Prometheus health
      ready      Check if Prometheus is ready
      config     Get Prometheus configuration
      flags      Get runtime flags
      runtime    Get version and runtime info
      tsdb       Get TSDB statistics
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
    """Check Prometheus health status.

    \b
    Examples:
      prometheus-mcp-server status health
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
    """Check if Prometheus is ready to serve queries.

    \b
    Examples:
      prometheus-mcp-server status ready
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
    """Get the current Prometheus configuration.

    \b
    Examples:
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
    """Get Prometheus runtime flags.

    \b
    Examples:
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
    """Get Prometheus version and runtime information.

    \b
    Examples:
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
    """Get TSDB (Time Series Database) statistics.

    \b
    Examples:
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
    """Get Prometheus build information.

    \b
    Examples:
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
    """Get WAL (Write-Ahead Log) replay status.

    Useful after Prometheus restart to check replay progress.

    \b
    Examples:
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
    """PromQL query utilities.

    \b
    Available commands:
      format    Format/prettify a PromQL query
      parse     Parse and validate a PromQL query
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

    \b
    Examples:
      prometheus-mcp-server promql format 'sum(rate(http_requests_total[5m]))by(status)'
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
    """Parse a PromQL query and return its AST representation.

    Useful for validating query syntax without executing.

    \b
    Examples:
      prometheus-mcp-server promql parse 'rate(http_requests_total[5m])'
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

    Verifies connectivity and authentication.

    \b
    Examples:
      prometheus-mcp-server check
      prometheus-mcp-server check --url https://prometheus.example.com
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

        # Get runtime info
        response = client.get("/api/v1/status/runtimeinfo")
        if response.success and response.data:
            version = response.data.get("version", "unknown")
            click.echo(f"  Prometheus version: {version}")
            click.echo(click.style("\nConnection successful!", fg="green", bold=True))
        else:
            click.echo(click.style(f"  Failed to get runtime info: {response.error}", fg="yellow"))

    except Exception as e:
        click.echo(click.style(f"\nConnection failed: {e}", fg="red", bold=True))
        sys.exit(1)
    finally:
        client.close()


@cli.command()
def info() -> None:
    """Display available MCP tools and CLI commands.

    Shows the mapping between MCP tools and CLI commands.
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
