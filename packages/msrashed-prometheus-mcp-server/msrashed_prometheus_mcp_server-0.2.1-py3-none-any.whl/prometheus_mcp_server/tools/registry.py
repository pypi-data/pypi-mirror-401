"""
Prometheus tools registry for MCP server.

All tools are READ-ONLY and use the Prometheus HTTP API.
"""

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from prometheus_mcp_server.utils.client import PrometheusClient
from prometheus_mcp_server.utils.helpers import parse_time


class PrometheusTools:
    """
    Register read-only Prometheus tools with MCP server.

    Provides comprehensive access to Prometheus monitoring data:
    - Queries: Instant and range queries with PromQL
    - Metadata: Metrics, labels, series discovery
    - Targets: Scrape targets and their status
    - Alerts: Active alerts and alert rules
    - Configuration: Prometheus config and runtime info
    """

    def __init__(
        self,
        mcp: FastMCP,
        url: str | None = None,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        """
        Initialize Prometheus tools.

        Args:
            mcp: FastMCP server instance
            url: Prometheus server URL
            token: Bearer token for authentication
            username: Username for basic auth
            password: Password for basic auth
            timeout: Request timeout in seconds
            verify_ssl: Verify SSL certificates
        """
        self.mcp = mcp
        self.url = url
        self.token = token
        self.username = username
        self.password = password
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._register_tools()

    def _get_client(self) -> PrometheusClient:
        """Create a new Prometheus client."""
        return PrometheusClient(
            url=self.url,
            token=self.token,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
            verify_ssl=self.verify_ssl,
        )

    def _format_response(self, response) -> str:
        """Format API response for MCP."""
        if response.success:
            result = {"data": response.data}
            if response.warnings:
                result["warnings"] = response.warnings
            return json.dumps(result, indent=2, default=str)
        else:
            return f"Error (HTTP {response.status_code}): {response.error}"

    def _register_tools(self) -> None:
        """Register all Prometheus tools with the MCP server."""

        # ============================================================
        # QUERY TOOLS
        # ============================================================

        @self.mcp.tool()
        def query_instant(
            query: str,
            time: str | None = None,
            timeout: str | None = None,
        ) -> str:
            """
            Execute a PromQL instant query at a single point in time.

            Use this tool to get current metric values or compute instant calculations.
            Returns a vector of time series with their current values. This is the most
            common query type for dashboards and alerts.

            Args:
                query: PromQL expression to evaluate (required). Common patterns:
                    - Simple metric: "up" (returns 1 for healthy targets, 0 for down)
                    - With label filter: "up{job='api-server', namespace='production'}"
                    - Rate calculation: "rate(http_requests_total[5m])" (per-second rate)
                    - Aggregation: "sum(rate(http_requests_total[5m])) by (status_code)"
                    - Math: "node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes"
                    - Histogram: "histogram_quantile(0.95, rate(x_bucket[5m]))"
                time: Evaluation timestamp (optional, defaults to current time). Formats:
                    - Relative: "now", "now-1h", "now-30m", "now-1d" (most convenient)
                    - RFC3339: "2024-01-15T10:00:00Z"
                    - Unix timestamp: "1705316400"
                timeout: Evaluation timeout (optional). Examples: "30s", "1m", "2m"

            Returns:
                JSON with resultType "vector" and array of {metric, value} objects.

            Examples:
                # Check which targets are up
                query_instant(query="up")

                # Get request rate for specific service
                query_instant(query="rate(http_requests_total{service='api'}[5m])")

                # Get value from 1 hour ago
                query_instant(query="up{job='prometheus'}", time="now-1h")

                # Calculate error rate percentage
                query_instant(query="sum(rate(http_requests_total{status=~'5..'}[5m]))/sum(rate(http_requests_total[5m]))")
            """
            params: dict[str, Any] = {"query": query}

            if time:
                parsed_time = parse_time(time)
                if parsed_time:
                    params["time"] = parsed_time

            if timeout:
                params["timeout"] = timeout

            with self._get_client() as client:
                response = client.get("/api/v1/query", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def query_range(
            query: str,
            start: str,
            end: str,
            step: str = "15s",
            timeout: str | None = None,
        ) -> str:
            """
            Execute a PromQL range query over a time period for graphing/trending.

            Use this tool to get metric values over time for charts, trend analysis,
            or historical comparisons. Returns multiple data points per series across
            the specified time range.

            Args:
                query: PromQL expression to evaluate (required). Best suited for:
                    - Rate metrics: "rate(http_requests_total[5m])"
                    - Aggregated rates: "sum(rate(http_requests_total[5m])) by (service)"
                    - Resource usage: "avg(container_memory_usage_bytes) by (pod)"
                    - Percentiles: "histogram_quantile(0.99, rate(x_bucket[5m]))"
                start: Start of time range (required). Formats:
                    - Relative: "now-1h", "now-6h", "now-1d", "now-7d" (most common)
                    - RFC3339: "2024-01-15T00:00:00Z"
                    - Unix timestamp: "1705276800"
                end: End of time range (required). Same formats as start.
                    - Typically "now" for current data
                step: Resolution step - time between data points (default: "15s").
                    - "15s" - High resolution, good for short ranges (<1h)
                    - "1m" - Medium resolution, good for 1-6h ranges
                    - "5m" - Lower resolution, good for 1d+ ranges
                    - Smaller step = more data points = larger response
                timeout: Evaluation timeout (optional). Examples: "30s", "1m", "5m"

            Returns:
                JSON with resultType "matrix" and array of {metric, values} objects.

            Examples:
                # Request rate over last hour
                query_range(query="rate(http_requests_total[5m])", start="now-1h", end="now")

                # CPU usage over last 6 hours
                query_range(
                    query="avg(rate(container_cpu_usage_seconds_total[5m])) by (container)",
                    start="now-6h", end="now", step="1m"
                )

                # P99 latency over last week
                query_range(
                    query="histogram_quantile(0.99, sum(rate(x_bucket[5m])) by (le))",
                    start="now-7d", end="now", step="15m"
                )
            """
            params: dict[str, Any] = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "step": step,
            }

            if timeout:
                params["timeout"] = timeout

            with self._get_client() as client:
                response = client.get("/api/v1/query_range", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def query_exemplars(
            query: str,
            start: str,
            end: str,
        ) -> str:
            """
            Query exemplars to correlate metrics with distributed traces.

            Exemplars are sample data points that link metrics (like histograms) to
            specific trace IDs. Use this for debugging specific requests that contributed
            to latency spikes or error rates. Requires Prometheus to be configured with
            exemplar storage and your metrics to include exemplar data.

            Args:
                query: PromQL selector for metrics with exemplars (required).
                    Typically histogram bucket metrics:
                    - "http_request_duration_seconds_bucket"
                    - "http_request_duration_seconds_bucket{service='api'}"
                    - "grpc_server_handling_seconds_bucket{grpc_method='GetUser'}"
                start: Start of time range (required). Formats: "now-1h", RFC3339, Unix timestamp.
                end: End of time range (required). Formats: "now", RFC3339, Unix timestamp.

            Returns:
                JSON with exemplar data including seriesLabels, exemplars, timestamp, value.

            Examples:
                # Get exemplars for HTTP request latency
                query_exemplars(
                    query="http_request_duration_seconds_bucket",
                    start="now-1h", end="now"
                )

                # Get exemplars for specific service
                query_exemplars(
                    query="http_request_duration_seconds_bucket{service='api'}",
                    start="now-30m", end="now"
                )
            """
            params = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
            }

            with self._get_client() as client:
                response = client.get("/api/v1/query_exemplars", params=params)
                return self._format_response(response)

        # ============================================================
        # METADATA TOOLS
        # ============================================================

        @self.mcp.tool()
        def list_metrics(match: str | None = None) -> str:
            """
            List all available metric names for discovery and exploration.

            Use this tool to discover what metrics are available in Prometheus.
            This is often the first step when exploring a new system or finding
            metrics to use in queries. Returns unique metric names (the __name__ label).

            Args:
                match: Series selector to filter metrics (optional).
                    Without this, returns ALL metric names which can be thousands.
                    Filter examples:
                    - "{job='api-server'}" - Metrics from specific job
                    - "{namespace='production'}" - Metrics from namespace
                    - "{__name__=~'http_.*'}" - Metrics starting with http_
                    - "{__name__=~'.*_total'}" - Counter metrics ending in _total

            Returns:
                JSON array of metric name strings.

            Examples:
                # List all available metrics (may return many results)
                list_metrics()

                # List metrics from a specific job
                list_metrics(match="{job='kubernetes-pods'}")

                # Find all HTTP-related metrics
                list_metrics(match="{__name__=~'http_.*'}")

                # Find metrics in production namespace
                list_metrics(match="{namespace='production'}")
            """
            params = {}
            if match:
                params["match[]"] = match

            with self._get_client() as client:
                response = client.get(
                    "/api/v1/label/__name__/values",
                    params=params if params else None,
                )
                return self._format_response(response)

        @self.mcp.tool()
        def get_metric_metadata(
            metric: str | None = None,
            limit: int | None = None,
        ) -> str:
            """
            Get metric type, help text, and unit information.

            Use this tool to understand what a metric measures and how to interpret it.
            Returns metadata that was defined when the metric was exposed, including:
            - type: counter, gauge, histogram, summary, or unknown
            - help: Description of what the metric measures
            - unit: Unit of measurement (if defined)

            Args:
                metric: Specific metric name to look up (optional).
                    Without this, returns metadata for ALL metrics.
                    Examples: "http_requests_total", "process_cpu_seconds_total"
                limit: Maximum number of metrics to return (optional).
                    Useful when querying all metrics: limit=100

            Returns:
                JSON object mapping metric names to metadata arrays (type, help, unit).

            Examples:
                # Get metadata for a specific metric
                get_metric_metadata(metric="http_requests_total")

                # Get metadata for process metrics
                get_metric_metadata(metric="process_cpu_seconds_total")

                # Get first 50 metrics' metadata
                get_metric_metadata(limit=50)

                # Understand a histogram metric
                get_metric_metadata(metric="http_request_duration_seconds")
            """
            params = {}
            if metric:
                params["metric"] = metric
            if limit:
                params["limit"] = limit

            with self._get_client() as client:
                response = client.get("/api/v1/metadata", params=params if params else None)
                return self._format_response(response)

        @self.mcp.tool()
        def list_labels(
            match: list[str] | None = None,
            start: str | None = None,
            end: str | None = None,
        ) -> str:
            """
            List all label names used across metrics.

            Use this tool to discover available labels for filtering queries.
            Labels are key-value pairs attached to metrics (e.g., job, instance,
            namespace, pod). Returns all unique label names.

            Args:
                match: Series selectors to filter which metrics to consider (optional).
                    List of PromQL selectors. Without filter, returns all labels.
                    Examples:
                    - ["{job='api-server'}"] - Labels from api-server metrics
                    - ["{namespace='production'}"] - Labels from production namespace
                    - ["{__name__='up'}"] - Labels on the 'up' metric
                start: Start timestamp (optional). Format: "now-1h", RFC3339, Unix.
                end: End timestamp (optional). Format: "now", RFC3339, Unix.

            Returns:
                JSON array of label name strings.

            Examples:
                # List all labels in Prometheus
                list_labels()

                # List labels available for a specific job
                list_labels(match=["{job='kubernetes-pods'}"])

                # List labels for HTTP metrics only
                list_labels(match=["{__name__=~'http_.*'}"])

                # List labels with time filter
                list_labels(match=["{job='api'}"], start="now-1h", end="now")
            """
            params = {}
            if match:
                params["match[]"] = match
            if start:
                params["start"] = parse_time(start)
            if end:
                params["end"] = parse_time(end)

            with self._get_client() as client:
                response = client.get("/api/v1/labels", params=params if params else None)
                return self._format_response(response)

        @self.mcp.tool()
        def get_label_values(
            label: str,
            match: list[str] | None = None,
            start: str | None = None,
            end: str | None = None,
        ) -> str:
            """
            Get all unique values for a specific label.

            Use this tool to discover what values exist for a label, helping you
            build filtered queries. For example, get all job names, all namespaces,
            all instance addresses, etc.

            Args:
                label: Label name to get values for (required).
                    Common labels:
                    - "job" - Scrape job names
                    - "instance" - Target addresses (host:port)
                    - "namespace" - Kubernetes namespaces
                    - "pod" - Pod names
                    - "container" - Container names
                    - "service" - Service names
                    - "__name__" - Metric names
                match: Series selectors to filter scope (optional).
                    Examples:
                    - ["{namespace='production'}"] - Values only from production
                    - ["{__name__='up'}"] - Values only from 'up' metric
                start: Start timestamp (optional). Format: "now-1h", RFC3339, Unix.
                end: End timestamp (optional). Format: "now", RFC3339, Unix.

            Returns:
                JSON array of unique label value strings.

            Examples:
                # Get all job names
                get_label_values(label="job")

                # Get all namespaces
                get_label_values(label="namespace")

                # Get instances for a specific job
                get_label_values(label="instance", match=["{job='api-server'}"])

                # Get pods in production namespace
                get_label_values(label="pod", match=["{namespace='production'}"])

                # Get all status codes used in HTTP metrics
                get_label_values(label="status_code", match=["{__name__=~'http_.*'}"])
            """
            params = {}
            if match:
                params["match[]"] = match
            if start:
                params["start"] = parse_time(start)
            if end:
                params["end"] = parse_time(end)

            with self._get_client() as client:
                response = client.get(
                    f"/api/v1/label/{label}/values",
                    params=params if params else None,
                )
                return self._format_response(response)

        @self.mcp.tool()
        def find_series(
            match: list[str],
            start: str | None = None,
            end: str | None = None,
        ) -> str:
            """
            Find all time series matching label selectors.

            Use this tool to discover what specific time series exist for given criteria.
            Unlike list_metrics which returns only names, this returns the full label
            set for each matching series. Useful for understanding cardinality and
            finding specific series to query.

            Args:
                match: List of series selectors (required). At least one selector required.
                    Each selector is a PromQL label matcher:
                    - ["{job='api-server'}"] - All series from api-server job
                    - ["{__name__='up'}"] - All 'up' metric series
                    - ["{namespace='production',job=~'.*-api'}"] - Production APIs
                    - ["{__name__=~'http_request.*'}"] - All HTTP request metrics
                    Multiple selectors: ["{job='a'}", "{job='b'}"] returns union of matches
                start: Start timestamp (optional). Format: "now-1h", RFC3339, Unix.
                end: End timestamp (optional). Format: "now", RFC3339, Unix.

            Returns:
                JSON array of objects, each containing the full label set for a matching series.

            Examples:
                # Find all series for a job
                find_series(match=["{job='api-server'}"])

                # Find all 'up' metric series to see what targets exist
                find_series(match=["{__name__='up'}"])

                # Find HTTP metrics in production
                find_series(match=["{__name__=~'http_.*', namespace='production'}"])

                # Find high-cardinality series (useful for debugging)
                find_series(match=["{__name__='http_requests_total'}"], start="now-1h", end="now")

                # Find series from multiple jobs
                find_series(match=["{job='frontend'}", "{job='backend'}"])
            """
            params = {"match[]": match}
            if start:
                params["start"] = parse_time(start)
            if end:
                params["end"] = parse_time(end)

            with self._get_client() as client:
                response = client.post("/api/v1/series", data=params)
                return self._format_response(response)

        # ============================================================
        # TARGET & SCRAPE TOOLS
        # ============================================================

        @self.mcp.tool()
        def list_targets(state: str = "any") -> str:
            """
            List all scrape targets and their current health status.

            Use this tool to check which targets Prometheus is scraping, their health,
            and troubleshoot scraping issues. Shows discovered targets, their labels,
            last scrape time, and any errors.

            Args:
                state: Filter targets by state (optional, default: "any").
                    - "any" - All targets (active and dropped)
                    - "active" - Only currently active/healthy targets being scraped
                    - "dropped" - Only dropped targets (filtered out by relabeling rules)

            Returns:
                JSON with activeTargets and droppedTargets arrays. Each target includes:
                - labels: Target labels (job, instance, etc.)
                - scrapePool: Scrape configuration name
                - scrapeUrl: Full URL being scraped
                - health: "up" or "down"
                - lastScrape: Timestamp of last scrape
                - lastScrapeDuration: How long the last scrape took
                - lastError: Error message if scrape failed

            Examples:
                # List all targets (active and dropped)
                list_targets()

                # List only active/healthy targets
                list_targets(state="active")

                # List dropped targets to debug relabeling
                list_targets(state="dropped")
            """
            params = {"state": state}

            with self._get_client() as client:
                response = client.get("/api/v1/targets", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def get_targets_metadata(
            match_target: str | None = None,
            metric: str | None = None,
            limit: int | None = None,
        ) -> str:
            """
            Get metric metadata reported by scrape targets.

            Use this tool to see what metrics a specific target exposes and their types.
            This metadata comes directly from the targets' /metrics endpoint, not from
            Prometheus's own metadata store.

            Args:
                match_target: Label selector to filter targets (optional).
                    Uses the same format as PromQL label matchers:
                    - "{job='api-server'}" - Metadata from api-server targets
                    - "{instance='localhost:9090'}" - Metadata from specific instance
                    - "{job=~'.*-exporter'}" - Metadata from all exporter jobs
                metric: Specific metric name to look up (optional).
                    Examples: "http_requests_total", "process_cpu_seconds_total"
                limit: Maximum number of results to return (optional).

            Returns:
                JSON array of metadata objects with target, metric, type, help, and unit.

            Examples:
                # Get all metadata from api-server targets
                get_targets_metadata(match_target="{job='api-server'}")

                # Get metadata for a specific metric across all targets
                get_targets_metadata(metric="http_requests_total")

                # Get metadata for specific metric from specific job
                get_targets_metadata(
                    match_target="{job='node-exporter'}", metric="node_cpu_seconds_total"
                )

                # Get first 100 metadata entries
                get_targets_metadata(limit=100)
            """
            params = {}
            if match_target:
                params["match_target"] = match_target
            if metric:
                params["metric"] = metric
            if limit:
                params["limit"] = limit

            with self._get_client() as client:
                response = client.get("/api/v1/targets/metadata", params=params if params else None)
                return self._format_response(response)

        # ============================================================
        # ALERT TOOLS
        # ============================================================

        @self.mcp.tool()
        def list_alerts() -> str:
            """
            List all currently active alerts (firing and pending).

            Use this tool to see what alerts are currently active in Prometheus.
            Shows both firing alerts (threshold exceeded for required duration)
            and pending alerts (threshold exceeded but not yet for full duration).

            Returns:
                JSON with alerts array. Each alert includes:
                - labels: Alert identity labels (alertname, severity, etc.)
                - annotations: Descriptive annotations (summary, description, etc.)
                - state: "firing" or "pending"
                - activeAt: When the alert became active
                - value: Current value that triggered the alert

            Examples:
                # List all active alerts
                list_alerts()

            Use list_rules(type="alert") to see all configured alerting rules.
            """
            with self._get_client() as client:
                response = client.get("/api/v1/alerts")
                return self._format_response(response)

        @self.mcp.tool()
        def list_rules(type: str | None = None) -> str:
            """
            List all configured recording and alerting rules.

            Use this tool to see rule definitions and their current evaluation status.
            Shows rules grouped by their rule files and rule groups.

            Args:
                type: Filter by rule type (optional).
                    - "alert" - Only alerting rules (rules that trigger alerts)
                    - "record" - Only recording rules (rules that precompute metrics)
                    - None - All rules (default)

            Returns:
                JSON with groups array. Each group contains:
                - name: Rule group name
                - file: Source file path
                - interval: Evaluation interval
                - rules: Array of rules with:
                    - For alerting rules: name, query, duration, labels, annotations, state, alerts
                    - For recording rules: name, query, labels, health, lastError

            Examples:
                # List all rules
                list_rules()

                # List only alerting rules
                list_rules(type="alert")

                # List only recording rules
                list_rules(type="record")
            """
            params = {}
            if type:
                params["type"] = type

            with self._get_client() as client:
                response = client.get("/api/v1/rules", params=params if params else None)
                return self._format_response(response)

        # ============================================================
        # CONFIGURATION & STATUS TOOLS
        # ============================================================

        @self.mcp.tool()
        def get_config() -> str:
            """
            Get the currently loaded Prometheus configuration.

            Use this tool to inspect how Prometheus is configured, including scrape
            configs, alerting rules, remote write/read settings, and more. Returns
            the full YAML configuration that was loaded at startup.

            Returns:
                JSON with yaml field containing the full Prometheus configuration as a YAML string.
                Configuration includes: global settings, scrape_configs, alerting rules,
                remote_write, remote_read, and storage settings.

            Examples:
                # Get full Prometheus configuration
                get_config()

            Note: Sensitive values may be redacted in the output.
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/config")
                return self._format_response(response)

        @self.mcp.tool()
        def get_flags() -> str:
            """
            Get Prometheus command-line flags and their current values.

            Use this tool to see how Prometheus was started, including storage paths,
            retention settings, web configuration, and feature flags.

            Returns:
                JSON object mapping flag names to their current values.
                Common flags include:
                - storage.tsdb.path: Data storage directory
                - storage.tsdb.retention.time: Data retention period
                - web.listen-address: HTTP server address
                - web.enable-lifecycle: If lifecycle endpoints are enabled
                - web.enable-admin-api: If admin API is enabled

            Examples:
                # Get all runtime flags
                get_flags()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/flags")
                return self._format_response(response)

        @self.mcp.tool()
        def get_runtime_info() -> str:
            """
            Get Prometheus server runtime information.

            Use this tool to get information about the running Prometheus instance,
            including version, uptime, storage status, and memory usage.

            Returns:
                JSON with runtime information including:
                - startTime: When Prometheus started
                - CWD: Current working directory
                - reloadConfigSuccess: If last config reload succeeded
                - lastConfigTime: When config was last reloaded
                - corruptionCount: Number of WAL corruptions detected
                - goroutineCount: Number of goroutines
                - GOMAXPROCS: Go max processors setting
                - GOGC: Go garbage collector setting
                - GODEBUG: Go debug settings
                - storageRetention: Data retention period

            Examples:
                # Get runtime information
                get_runtime_info()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/runtimeinfo")
                return self._format_response(response)

        @self.mcp.tool()
        def get_tsdb_stats() -> str:
            """
            Get TSDB (Time Series Database) cardinality and storage statistics.

            Use this tool to analyze storage usage, identify high-cardinality metrics,
            and understand the size of your Prometheus data. Useful for capacity
            planning and debugging cardinality issues.

            Returns:
                JSON with TSDB statistics including:
                - headStats: Current head block info (numSeries, numChunks, numSamples)
                - seriesCountByMetricName: Top metrics by series count (cardinality)
                - labelValueCountByLabelName: Top labels by unique value count
                - memoryInBytesByLabelName: Memory usage by label
                - seriesCountByLabelValuePair: Top label-value pairs by series count

            Examples:
                # Get TSDB statistics to analyze cardinality
                get_tsdb_stats()

            Use this to identify:
            - High-cardinality metrics causing storage bloat
            - Labels with too many unique values
            - Overall series count and storage usage
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/tsdb")
                return self._format_response(response)

        @self.mcp.tool()
        def check_health() -> str:
            """
            Check if Prometheus server is healthy.

            Use this tool to verify Prometheus is running and responding to requests.
            This is a basic liveness check - it returns healthy if Prometheus is up.

            Returns:
                JSON with status: "healthy" or "unhealthy" with error details.

            Examples:
                # Check if Prometheus is healthy
                check_health()

            For query readiness, use check_readiness() instead.
            """
            with self._get_client() as client:
                response = client.get("/-/healthy")
                if response.status_code == 200:
                    return json.dumps({"status": "healthy"}, indent=2)
                else:
                    return json.dumps({"status": "unhealthy", "error": response.error}, indent=2)

        @self.mcp.tool()
        def check_readiness() -> str:
            """
            Check if Prometheus is ready to serve queries.

            Use this tool to verify Prometheus has completed startup and is ready
            to handle queries. Unlike health check, readiness considers whether
            WAL replay is complete and the server can serve accurate data.

            Returns:
                JSON with status: "ready" or "not_ready" with error details.

            Examples:
                # Check if Prometheus is ready for queries
                check_readiness()

            Use after Prometheus restart to verify it's ready before querying.
            """
            with self._get_client() as client:
                response = client.get("/-/ready")
                if response.status_code == 200:
                    return json.dumps({"status": "ready"}, indent=2)
                else:
                    return json.dumps({"status": "not_ready", "error": response.error}, indent=2)

        @self.mcp.tool()
        def get_build_info() -> str:
            """
            Get Prometheus server build and version information.

            Use this tool to identify which version of Prometheus is running and
            how it was built. Useful for compatibility checks and troubleshooting.

            Returns:
                JSON with build information including:
                - version: Prometheus version (e.g., "2.47.0")
                - revision: Git commit hash
                - branch: Git branch name
                - buildUser: Who built this binary
                - buildDate: When it was built
                - goVersion: Go compiler version used

            Examples:
                # Get Prometheus version and build info
                get_build_info()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/buildinfo")
                return self._format_response(response)

        @self.mcp.tool()
        def get_wal_replay_status() -> str:
            """
            Get WAL (Write-Ahead Log) replay progress after Prometheus restart.

            Use this tool after Prometheus restarts to monitor WAL replay progress.
            WAL replay restores in-memory data from the write-ahead log, which can
            take time for large datasets.

            Returns:
                JSON with WAL replay status including:
                - min: First WAL segment to replay
                - max: Last WAL segment to replay
                - current: Currently replaying segment
                - state: Current replay state

            Examples:
                # Check WAL replay progress after restart
                get_wal_replay_status()

            Note: Once replay is complete, values converge (min ≈ max ≈ current).
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/walreplay")
                return self._format_response(response)

        # ============================================================
        # UTILITY TOOLS
        # ============================================================

        @self.mcp.tool()
        def format_query(query: str) -> str:
            """
            Format and prettify a PromQL query expression.

            Use this tool to clean up and standardize PromQL query formatting.
            The Prometheus server parses and re-serializes the query with
            consistent spacing and structure.

            Args:
                query: PromQL expression to format (required).
                    Can be any valid PromQL query, even poorly formatted:
                    - "sum(rate(http_requests_total[5m]))by(status)" → formatted
                    - "up{job='api'}" → standardized label format

            Returns:
                JSON with data field containing the formatted query string.

            Examples:
                # Format a compact query
                format_query(query="sum(rate(http_requests_total[5m]))by(status)")
                # Returns: "sum by (status) (rate(http_requests_total[5m]))"

                # Format query with inconsistent spacing
                format_query(query="rate(  http_requests_total{job='api'}[5m])")
                # Returns: "rate(http_requests_total{job='api'}[5m])"

                # Validate and format complex query
                format_query(query="histogram_quantile(0.99,sum(rate(http_request_duration_seconds_bucket[5m]))by(le))")
            """
            params = {"query": query}

            with self._get_client() as client:
                response = client.get("/api/v1/format_query", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def parse_query(query: str) -> str:
            """
            Parse a PromQL query and return its Abstract Syntax Tree (AST).

            Use this tool to validate PromQL syntax without executing the query,
            or to understand how Prometheus interprets a query. Returns the parsed
            structure showing operators, functions, selectors, and their relationships.

            Args:
                query: PromQL expression to parse (required).
                    Any PromQL query:
                    - "up" - Simple metric selector
                    - "rate(http_requests_total[5m])" - Function call
                    - "sum(rate(x[5m])) by (job)" - Aggregation

            Returns:
                JSON with data field containing the AST structure. For invalid queries,
                returns an error with the parse error message and position.

            Examples:
                # Parse a simple metric
                parse_query(query="up")
                # Returns: {"type": "vectorSelector", "name": "up", ...}

                # Parse a rate function
                parse_query(query="rate(http_requests_total[5m])")
                # Returns: {"type": "call", "func": {"name": "rate"}, ...}

                # Validate query syntax (invalid query)
                parse_query(query="rate(http_requests_total[5m]")
                # Returns: Error with parse error message

                # Understand complex query structure
                parse_query(query="histogram_quantile(0.99, sum(rate(x_bucket[5m])) by (le))")
            """
            params = {"query": query}

            with self._get_client() as client:
                response = client.get("/api/v1/parse_query", params=params)
                return self._format_response(response)
