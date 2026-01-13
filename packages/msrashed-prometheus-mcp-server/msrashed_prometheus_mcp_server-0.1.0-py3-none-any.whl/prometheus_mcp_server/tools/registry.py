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

            Args:
                query: PromQL expression to evaluate.
                    Examples:
                    - "up" - Check which targets are up
                    - "up{job='api-server'}" - Filter by label
                    - "rate(http_requests_total[5m])" - Request rate
                    - "sum(rate(http_requests_total[5m])) by (status)" - Aggregated rate
                time: Evaluation timestamp. Formats:
                    - RFC3339: "2024-01-15T10:00:00Z"
                    - Unix timestamp: "1705316400"
                    - Relative: "now", "now-1h"
                    - Default: current time
                timeout: Evaluation timeout (e.g., "30s", "1m")

            Returns:
                Query result with instant vector data.

            Example:
                query_instant(
                    query="up{job='prometheus'}",
                    time="now"
                )
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
            Execute a PromQL range query over a period of time.

            Args:
                query: PromQL expression to evaluate.
                    Examples:
                    - "rate(http_requests_total[5m])" - Request rate over time
                    - "avg(cpu_usage) by (instance)" - Average CPU by instance
                start: Start timestamp. Formats:
                    - RFC3339: "2024-01-15T00:00:00Z"
                    - Unix timestamp: "1705276800"
                    - Relative: "now-6h"
                end: End timestamp (same formats as start).
                step: Query resolution step (e.g., "15s", "1m", "5m").
                    Controls data point density.
                timeout: Evaluation timeout (e.g., "30s", "1m")

            Returns:
                Query result with range vector data over time.

            Example:
                query_range(
                    query="rate(http_requests_total[5m])",
                    start="now-1h",
                    end="now",
                    step="30s"
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
            Query exemplars for a metric (links metrics to traces).

            Exemplars are references to data outside of the metrics themselves.
            Commonly used for trace IDs to correlate metrics with traces.

            Args:
                query: PromQL metric selector (e.g., "http_request_duration_seconds_bucket")
                start: Start timestamp
                end: End timestamp

            Returns:
                Exemplar data with trace IDs and values.

            Example:
                query_exemplars(
                    query="http_request_duration_seconds_bucket",
                    start="now-1h",
                    end="now"
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
            List all metric names available in Prometheus.

            Args:
                match: Optional metric name filter (regex pattern).
                    Examples:
                    - "http_.*" - All HTTP metrics
                    - ".*_total" - All counter metrics
                    - None - All metrics

            Returns:
                List of metric names.

            Example:
                list_metrics(match="http_.*")
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
            Get metadata (type, help text) for metrics.

            Args:
                metric: Specific metric name (returns all if None)
                limit: Maximum number of metrics to return

            Returns:
                Metric metadata including type and help text.

            Example:
                get_metric_metadata(metric="http_requests_total")
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
            List all label names.

            Args:
                match: Label matchers to filter (e.g., ['{job="api"}'])
                start: Start timestamp for filtering
                end: End timestamp for filtering

            Returns:
                List of label names.

            Example:
                list_labels(match=['{job="api-server"}'])
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
            Get all values for a specific label.

            Args:
                label: Label name (e.g., "job", "instance", "namespace")
                match: Label matchers to filter
                start: Start timestamp for filtering
                end: End timestamp for filtering

            Returns:
                List of unique values for the label.

            Example:
                get_label_values(label="job")
                get_label_values(label="namespace", match=['{cluster="prod"}'])
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
            Find time series that match label sets.

            Args:
                match: List of series selectors.
                    Examples:
                    - ['{job="api"}'] - All series for job=api
                    - ['{__name__=~"http_.*"}'] - All HTTP metrics
                start: Start timestamp
                end: End timestamp

            Returns:
                List of matching time series with their labels.

            Example:
                find_series(
                    match=['{job="api",namespace="production"}'],
                    start="now-1h",
                    end="now"
                )
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
            List all scrape targets and their status.

            Args:
                state: Filter by target state:
                    - "any" - All targets (default)
                    - "active" - Only active targets
                    - "dropped" - Only dropped targets

            Returns:
                List of targets with health status, labels, and last scrape info.

            Example:
                list_targets(state="active")
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
            Get metadata about metrics scraped from targets.

            Args:
                match_target: Label selectors to filter targets (e.g., '{job="api"}')
                metric: Filter by specific metric name
                limit: Maximum results to return

            Returns:
                Metric metadata from targets.

            Example:
                get_targets_metadata(match_target='{job="api-server"}')
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
            List all active alerts (firing and pending).

            Returns:
                Active alerts with their state, labels, annotations, and active time.

            Example:
                list_alerts()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/alerts")
                return self._format_response(response)

        @self.mcp.tool()
        def list_rules(type: str | None = None) -> str:
            """
            List all recording and alerting rules.

            Args:
                type: Filter by rule type:
                    - "alert" - Only alerting rules
                    - "record" - Only recording rules
                    - None - All rules (default)

            Returns:
                All rules grouped by file and group, with their configuration and health.

            Example:
                list_rules(type="alert")
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
            Get the current Prometheus configuration.

            Returns:
                Prometheus configuration YAML.

            Example:
                get_config()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/config")
                return self._format_response(response)

        @self.mcp.tool()
        def get_flags() -> str:
            """
            Get Prometheus runtime flags.

            Returns:
                All command-line flags and their values.

            Example:
                get_flags()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/flags")
                return self._format_response(response)

        @self.mcp.tool()
        def get_runtime_info() -> str:
            """
            Get Prometheus runtime information.

            Returns:
                Version, storage, startup time, and other runtime info.

            Example:
                get_runtime_info()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/runtimeinfo")
                return self._format_response(response)

        @self.mcp.tool()
        def get_tsdb_stats() -> str:
            """
            Get TSDB (Time Series Database) statistics.

            Returns:
                Cardinality statistics, head stats, and storage information.

            Example:
                get_tsdb_stats()
            """
            with self._get_client() as client:
                response = client.get("/api/v1/status/tsdb")
                return self._format_response(response)

        @self.mcp.tool()
        def check_health() -> str:
            """
            Check Prometheus health status.

            Returns:
                Health status (returns "ok" if healthy).

            Example:
                check_health()
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

            Returns:
                Readiness status.

            Example:
                check_readiness()
            """
            with self._get_client() as client:
                response = client.get("/-/ready")
                if response.status_code == 200:
                    return json.dumps({"status": "ready"}, indent=2)
                else:
                    return json.dumps({"status": "not_ready", "error": response.error}, indent=2)
