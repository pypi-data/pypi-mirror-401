"""Helper utilities for Prometheus MCP server."""

import re
from datetime import UTC, datetime

from dateutil import parser as dateparser


def parse_time(time_str: str | int | float | None) -> str | None:
    """
    Parse various time formats to RFC3339 or Unix timestamp.

    Args:
        time_str: Time in various formats:
            - RFC3339: "2024-01-15T10:00:00Z"
            - Unix timestamp: 1705316400
            - Relative: "now", "now-1h", "now-6h"
            - None: returns None

    Returns:
        Formatted time string suitable for Prometheus API
    """
    if time_str is None:
        return None

    # If it's already a number (Unix timestamp), convert to string
    if isinstance(time_str, (int, float)):
        return str(time_str)

    # Handle "now" and relative times
    if isinstance(time_str, str):
        if time_str == "now":
            return str(int(datetime.now(UTC).timestamp()))

        # Handle relative time like "now-1h", "now-30m", "now-1d"
        if time_str.startswith("now-") or time_str.startswith("now+"):
            now = datetime.now(UTC).timestamp()
            offset_str = time_str[4:]  # Remove "now-" or "now+"
            try:
                offset_seconds = parse_duration_to_seconds(offset_str)
                if time_str.startswith("now-"):
                    return str(int(now - offset_seconds))
                else:
                    return str(int(now + offset_seconds))
            except ValueError:
                # If parsing fails, return as-is
                return time_str

        # Try parsing as RFC3339 or ISO8601
        try:
            dt = dateparser.isoparse(time_str)
            return str(int(dt.timestamp()))
        except (ValueError, TypeError):
            # If parsing fails, return as-is and let Prometheus handle it
            return time_str

    return str(time_str)


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Human-readable duration (e.g., "1.5s", "2m 30s", "1h 15m")
    """
    if seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        if secs > 0:
            return f"{minutes}m {secs:.0f}s"
        return f"{minutes}m"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"


def parse_duration_to_seconds(duration: str) -> float:
    """
    Parse Prometheus duration string to seconds.

    Args:
        duration: Duration string (e.g., "5m", "1h", "30s", "1d")

    Returns:
        Duration in seconds
    """
    # Regex pattern for duration: number + unit
    pattern = r"(\d+(?:\.\d+)?)(ms|s|m|h|d|w|y)"
    matches = re.findall(pattern, duration.lower())

    if not matches:
        raise ValueError(f"Invalid duration format: {duration}")

    total_seconds = 0.0
    for value, unit in matches:
        num = float(value)
        if unit == "ms":
            total_seconds += num / 1000
        elif unit == "s":
            total_seconds += num
        elif unit == "m":
            total_seconds += num * 60
        elif unit == "h":
            total_seconds += num * 3600
        elif unit == "d":
            total_seconds += num * 86400
        elif unit == "w":
            total_seconds += num * 604800
        elif unit == "y":
            total_seconds += num * 31536000

    return total_seconds


def validate_promql_query(query: str) -> bool:
    """
    Basic validation of PromQL query syntax.

    Args:
        query: PromQL query string

    Returns:
        True if query appears valid, False otherwise
    """
    if not query or not query.strip():
        return False

    # Basic checks
    query = query.strip()

    # Check for balanced braces and parentheses
    if query.count("{") != query.count("}"):
        return False
    if query.count("(") != query.count(")"):
        return False
    return query.count("[") == query.count("]")


def format_query_result(result: dict) -> str:
    """
    Format Prometheus query result for display.

    Args:
        result: Query result from Prometheus API

    Returns:
        Formatted string representation
    """
    result_type = result.get("resultType")
    data = result.get("result", [])

    if result_type == "matrix":
        # Range query result
        output = []
        for series in data:
            metric = series.get("metric", {})
            values = series.get("values", [])
            metric_str = ", ".join(f'{k}="{v}"' for k, v in metric.items())
            output.append(f"{{{metric_str}}} => {len(values)} data points")
        return "\n".join(output) if output else "No data"

    elif result_type == "vector":
        # Instant query result
        output = []
        for series in data:
            metric = series.get("metric", {})
            value = series.get("value", [])
            metric_str = ", ".join(f'{k}="{v}"' for k, v in metric.items())
            if len(value) == 2:
                timestamp, val = value
                output.append(f"{{{metric_str}}} => {val}")
        return "\n".join(output) if output else "No data"

    elif result_type == "scalar":
        # Scalar result
        if data and len(data) == 2:
            return f"Scalar value: {data[1]}"
        return "No data"

    elif result_type == "string":
        # String result
        if data and len(data) == 2:
            return f"String value: {data[1]}"
        return "No data"

    return str(data)
