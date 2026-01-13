"""LogQL query helpers for Loki MCP server."""

import re
from typing import Any


def validate_logql_query(query: str) -> bool:
    """
    Basic validation of LogQL query syntax.

    Args:
        query: LogQL query string

    Returns:
        True if query appears valid, False otherwise
    """
    if not query or not query.strip():
        return False

    query = query.strip()

    # Check for balanced braces, parentheses, and brackets
    if query.count("{") != query.count("}"):
        return False
    if query.count("(") != query.count(")"):
        return False
    if query.count("[") != query.count("]"):
        return False

    # Must have at least one label selector
    return "{" in query


def build_label_selector(labels: dict[str, str]) -> str:
    """
    Build LogQL label selector from dictionary.

    Args:
        labels: Dictionary of label key-value pairs

    Returns:
        LogQL label selector string

    Example:
        >>> build_label_selector({"namespace": "production", "app": "api"})
        '{namespace="production",app="api"}'
    """
    if not labels:
        return "{}"

    pairs = [f'{key}="{value}"' for key, value in labels.items()]
    return "{" + ",".join(pairs) + "}"


def extract_label_selectors(query: str) -> list[dict[str, str]]:
    """
    Extract label selectors from LogQL query.

    Args:
        query: LogQL query string

    Returns:
        List of label selector dictionaries
    """
    selectors = []

    # Find all label selectors in braces
    pattern = r"\{([^}]+)\}"
    matches = re.findall(pattern, query)

    for match in matches:
        labels = {}
        # Parse key-value pairs
        pairs = match.split(",")
        for pair in pairs:
            pair = pair.strip()
            if "=" in pair:
                key, value = pair.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                labels[key] = value

        if labels:
            selectors.append(labels)

    return selectors


def is_metric_query(query: str) -> bool:
    """
    Check if query is a metric query (returns numbers) vs log query (returns logs).

    Metric queries use aggregation functions like:
    - rate(), count_over_time(), bytes_over_time()
    - sum(), avg(), min(), max(), count()

    Args:
        query: LogQL query string

    Returns:
        True if query is a metric query
    """
    metric_functions = [
        "rate(",
        "count_over_time(",
        "bytes_over_time(",
        "bytes_rate(",
        "sum(",
        "avg(",
        "min(",
        "max(",
        "count(",
        "stddev(",
        "stdvar(",
        "quantile(",
        "topk(",
        "bottomk(",
    ]

    query_lower = query.lower()
    return any(func in query_lower for func in metric_functions)


def format_log_result(result: dict[str, Any]) -> str:
    """
    Format Loki log query result for display.

    Args:
        result: Query result from Loki API

    Returns:
        Formatted string representation
    """
    from loki_mcp_server.utils.helpers import format_timestamp

    result_type = result.get("resultType")
    data = result.get("result", [])

    if not data:
        return "No logs found"

    if result_type == "streams":
        # Log stream result
        output = []
        total_entries = 0

        for stream in data:
            labels = stream.get("stream", {})
            entries = stream.get("values", [])
            total_entries += len(entries)

            label_str = ", ".join(f'{k}="{v}"' for k, v in labels.items())
            output.append(f"\nStream: {{{label_str}}}")
            output.append(f"Entries: {len(entries)}")

            # Show first few entries
            for ts, line in entries[:5]:
                timestamp = format_timestamp(ts)
                output.append(f"  [{timestamp}] {line}")

            if len(entries) > 5:
                output.append(f"  ... and {len(entries) - 5} more entries")

        output.insert(0, f"Total streams: {len(data)}, Total entries: {total_entries}")
        return "\n".join(output)

    elif result_type == "matrix":
        # Metric query result (range)
        output = []
        for series in data:
            metric = series.get("metric", {})
            values = series.get("values", [])
            metric_str = ", ".join(f'{k}="{v}"' for k, v in metric.items())
            output.append(f"{{{metric_str}}} => {len(values)} data points")
        return "\n".join(output) if output else "No data"

    elif result_type == "vector":
        # Metric query result (instant)
        output = []
        for series in data:
            metric = series.get("metric", {})
            value = series.get("value", [])
            metric_str = ", ".join(f'{k}="{v}"' for k, v in metric.items())
            if len(value) == 2:
                timestamp, val = value
                output.append(f"{{{metric_str}}} => {val}")
        return "\n".join(output) if output else "No data"

    return str(data)


def build_error_query(namespace: str | None = None, service: str | None = None) -> str:
    """
    Build LogQL query to find errors.

    Args:
        namespace: Kubernetes namespace filter
        service: Service name filter

    Returns:
        LogQL query string
    """
    labels = {}
    if namespace:
        labels["namespace"] = namespace
    if service:
        labels["app"] = service

    selector = build_label_selector(labels) if labels else "{}"

    # Search for common error patterns
    return f'{selector} |~ "(?i)(error|exception|fatal|panic|fail)"'


def build_trace_query(trace_id: str, start: str | None = None, end: str | None = None) -> str:
    """
    Build LogQL query to find logs for a trace ID.

    Args:
        trace_id: Trace ID to search for
        start: Start time
        end: End time

    Returns:
        LogQL query string
    """
    # Search for trace ID in various formats
    return f'{{}} |= "{trace_id}"'


def build_context_query(
    labels: dict[str, str], timestamp: str, before_seconds: int = 60, after_seconds: int = 60
) -> tuple[str, str, str]:
    """
    Build query parameters to get logs before and after a timestamp.

    Args:
        labels: Label selectors for the stream
        timestamp: Target timestamp (nanoseconds)
        before_seconds: Seconds before timestamp
        after_seconds: Seconds after timestamp

    Returns:
        Tuple of (query, start_time, end_time)
    """
    ts_ns = int(timestamp)
    start_ns = ts_ns - (before_seconds * 1_000_000_000)
    end_ns = ts_ns + (after_seconds * 1_000_000_000)

    selector = build_label_selector(labels)

    return selector, str(start_ns), str(end_ns)
