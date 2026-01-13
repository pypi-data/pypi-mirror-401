"""Helper utilities for Loki MCP server."""

import re
from datetime import UTC, datetime

from dateutil import parser as dateparser


def parse_time(time_str: str | int | float | None) -> str | None:
    """
    Parse various time formats to Unix nanoseconds for Loki API.

    Args:
        time_str: Time in various formats:
            - RFC3339: "2024-01-15T10:00:00Z"
            - Unix timestamp: 1705316400
            - Relative: "now", "now-1h", "now-6h"
            - None: returns None

    Returns:
        Formatted time string suitable for Loki API (Unix nanoseconds)
    """
    if time_str is None:
        return None

    # If it's already a number (Unix timestamp), convert to nanoseconds
    if isinstance(time_str, (int, float)):
        # If it looks like seconds (small number), convert to nanoseconds
        if time_str < 10000000000:  # Definitely seconds
            return str(int(time_str * 1_000_000_000))
        # If it's already in nanoseconds
        elif time_str > 1000000000000000000:
            return str(int(time_str))
        # Milliseconds
        elif time_str > 1000000000000:
            return str(int(time_str * 1_000_000))
        else:
            return str(int(time_str * 1_000_000_000))

    # Handle "now" and relative times
    if isinstance(time_str, str):
        if time_str == "now":
            return str(int(datetime.now(UTC).timestamp() * 1_000_000_000))

        # Handle relative time like "now-1h", "now+1h"
        if time_str.startswith("now-") or time_str.startswith("now+"):
            now = datetime.now(UTC).timestamp()
            offset_str = time_str[4:]  # Remove "now-" or "now+"
            try:
                offset_seconds = parse_duration_to_seconds(offset_str)
                if time_str.startswith("now-"):
                    return str(int((now - offset_seconds) * 1_000_000_000))
                else:
                    return str(int((now + offset_seconds) * 1_000_000_000))
            except ValueError:
                # If parsing fails, return as-is
                return time_str

        # Try parsing as RFC3339 or ISO8601
        try:
            dt = dateparser.isoparse(time_str)
            return str(int(dt.timestamp() * 1_000_000_000))
        except (ValueError, TypeError):
            # If parsing fails, return as-is and let Loki handle it
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
    Parse duration string to seconds.

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

    # Basic checks
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


def format_log_result(result: dict) -> str:
    """
    Format Loki log query result for display.

    Args:
        result: Query result from Loki API

    Returns:
        Formatted string representation
    """
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


def format_timestamp(nanoseconds: int | str) -> str:
    """
    Format Unix nanoseconds timestamp to human-readable string.

    Args:
        nanoseconds: Unix timestamp in nanoseconds

    Returns:
        ISO8601 formatted timestamp
    """
    try:
        ns = int(nanoseconds)
        seconds = ns / 1_000_000_000
        dt = datetime.fromtimestamp(seconds, tz=UTC)
        return dt.isoformat()
    except Exception:
        return str(nanoseconds)
