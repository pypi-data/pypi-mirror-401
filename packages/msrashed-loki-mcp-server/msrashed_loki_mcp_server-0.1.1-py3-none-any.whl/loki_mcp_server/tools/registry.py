"""
Loki tools registry for MCP server.

All tools are READ-ONLY and use the Loki HTTP API.
"""

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from loki_mcp_server.utils.client import LokiClient
from loki_mcp_server.utils.logql import (
    build_context_query,
    build_error_query,
    build_trace_query,
)
from loki_mcp_server.utils.time import parse_time


class LokiTools:
    """
    Register read-only Loki tools with MCP server.

    Provides comprehensive access to Loki log data:
    - Queries: Instant, range, and tail queries with LogQL
    - Labels: Label and series discovery
    - Analysis: Error patterns, log frequency, context gathering
    - Investigation: Trace correlation, error spikes, surrounding logs
    """

    def __init__(
        self,
        mcp: FastMCP,
        url: str | None = None,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        org_id: str | None = None,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        """
        Initialize Loki tools.

        Args:
            mcp: FastMCP server instance
            url: Loki server URL
            token: Bearer token for authentication
            username: Username for basic auth
            password: Password for basic auth
            org_id: Organization ID for multi-tenancy
            timeout: Request timeout in seconds
            verify_ssl: Verify SSL certificates
        """
        self.mcp = mcp
        self.url = url
        self.token = token
        self.username = username
        self.password = password
        self.org_id = org_id
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._register_tools()

    def _get_client(self) -> LokiClient:
        """Create a new Loki client."""
        return LokiClient(
            url=self.url,
            token=self.token,
            username=self.username,
            password=self.password,
            org_id=self.org_id,
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
        """Register all Loki tools with the MCP server."""

        # ============================================================
        # CORE QUERY TOOLS (Epic 1)
        # ============================================================

        @self.mcp.tool()
        def query_logs(
            query: str,
            time: str | None = None,
            limit: int = 100,
            direction: str = "backward",
        ) -> str:
            """
            Execute a LogQL instant query at a specific point in time.

            Args:
                query: LogQL query expression.
                    Examples:
                    - '{namespace="production",app="api"}' - Basic selector
                    - '{job="api-server"} |= "error"' - Text filter
                    - '{app="api"} | json | level="error"' - JSON parsing
                    - '{job="nginx"} | logfmt | status>=500' - Logfmt parsing
                time: Evaluation timestamp. Formats:
                    - RFC3339: "2024-01-15T10:00:00Z"
                    - Unix timestamp: "1705316400"
                    - Relative: "now", "now-1h"
                    - Default: current time
                limit: Maximum number of log entries to return (default: 100)
                direction: Return direction - "forward" or "backward" (default: backward)

            Returns:
                Log entries with labels and timestamps.

            Example:
                query_logs(
                    query='{namespace="production",app="api"} |= "error" | json',
                    limit=100,
                    time="2024-01-15T10:00:00Z"
                )
            """
            params: dict[str, Any] = {
                "query": query,
                "limit": limit,
                "direction": direction,
            }

            if time:
                parsed_time = parse_time(time)
                if parsed_time:
                    params["time"] = parsed_time

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def query_logs_range(
            query: str,
            start: str,
            end: str,
            limit: int = 1000,
            direction: str = "backward",
            step: str | None = None,
        ) -> str:
            """
            Execute a LogQL query over a time range.

            Supports both log queries (returns log lines) and metric queries
            (returns numeric values).

            Args:
                query: LogQL query expression.
                    Log queries:
                    - '{job="api-server"} |= "error"'
                    Metric queries:
                    - 'rate({namespace="production"}[5m])'
                    - 'sum(rate({app="api"}[1m])) by (status_code)'
                    - 'count_over_time({job="api"}[10m])'
                start: Start timestamp. Formats:
                    - RFC3339: "2024-01-15T00:00:00Z"
                    - Unix timestamp: "1705276800"
                    - Relative: "now-6h"
                end: End timestamp (same formats as start).
                limit: Maximum number of entries (for log queries, default: 1000)
                direction: Return direction - "forward" or "backward" (default: backward)
                step: Query resolution for metric queries (e.g., "15s", "1m", "5m")

            Returns:
                Log entries or metric data over the time range.

            Example:
                query_logs_range(
                    query='{job="api-server"} |= "error"',
                    start="2024-01-15T09:00:00Z",
                    end="2024-01-15T10:00:00Z",
                    limit=1000,
                    direction="backward"
                )
            """
            params: dict[str, Any] = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "limit": limit,
                "direction": direction,
            }

            if step:
                params["step"] = step

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        # ============================================================
        # LABEL & SERIES DISCOVERY TOOLS (Epic 2)
        # ============================================================

        @self.mcp.tool()
        def list_labels(
            start: str | None = None,
            end: str | None = None,
        ) -> str:
            """
            List all available label names.

            Useful for discovering what dimensions are available for filtering logs.
            Common labels include: job, namespace, pod, container, app, env, etc.

            Args:
                start: Start timestamp for filtering (optional)
                end: End timestamp for filtering (optional)

            Returns:
                List of label names.

            Example:
                list_labels(
                    start="2024-01-15T00:00:00Z",
                    end="2024-01-15T23:59:59Z"
                )
            """
            params = {}
            if start:
                params["start"] = parse_time(start)
            if end:
                params["end"] = parse_time(end)

            with self._get_client() as client:
                response = client.get("/loki/api/v1/labels", params=params if params else None)
                return self._format_response(response)

        @self.mcp.tool()
        def get_label_values(
            label: str,
            start: str | None = None,
            end: str | None = None,
            query: str | None = None,
        ) -> str:
            """
            Get all values for a specific label.

            Args:
                label: Label name (e.g., "namespace", "job", "app", "pod")
                start: Start timestamp for filtering (optional)
                end: End timestamp for filtering (optional)
                query: Additional LogQL query to filter results (optional)

            Returns:
                List of unique values for the label.

            Example:
                get_label_values(
                    label="namespace",
                    start="2024-01-15T00:00:00Z",
                    end="2024-01-15T23:59:59Z"
                )
            """
            params = {}
            if start:
                params["start"] = parse_time(start)
            if end:
                params["end"] = parse_time(end)
            if query:
                params["query"] = query

            with self._get_client() as client:
                response = client.get(
                    f"/loki/api/v1/label/{label}/values",
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
            Find log series that match label selectors.

            A series is a unique combination of labels that identifies a log stream.

            Args:
                match: List of series selectors.
                    Examples:
                    - ['{namespace="production"}']
                    - ['{job="api",env="prod"}']
                    - ['{namespace="production",app="api"}', '{namespace="staging"}']
                start: Start timestamp for filtering (optional)
                end: End timestamp for filtering (optional)

            Returns:
                List of matching series with their label sets.

            Example:
                find_series(
                    match=['{namespace="production"}', '{job="api"}'],
                    start="2024-01-15T00:00:00Z",
                    end="2024-01-15T23:59:59Z"
                )
            """
            params = {"match[]": match}
            if start:
                params["start"] = parse_time(start)
            if end:
                params["end"] = parse_time(end)

            with self._get_client() as client:
                response = client.get("/loki/api/v1/series", params=params)
                return self._format_response(response)

        # ============================================================
        # METRICS & STATISTICS TOOLS (Epic 3)
        # ============================================================

        @self.mcp.tool()
        def get_index_stats(
            query: str,
            start: str,
            end: str,
        ) -> str:
            """
            Get index statistics for a query.

            Shows chunk and stream statistics, useful for understanding
            log volume and query performance.

            Args:
                query: LogQL query to analyze
                start: Start timestamp
                end: End timestamp

            Returns:
                Index statistics including streams, chunks, bytes, entries.

            Example:
                get_index_stats(
                    query='{namespace="production"}',
                    start="2024-01-15T00:00:00Z",
                    end="2024-01-15T23:59:59Z"
                )
            """
            params = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/index/stats", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def query_log_volume(
            query: str,
            start: str,
            end: str,
            step: str = "5m",
            limit: int = 5000,
        ) -> str:
            """
            Query log volume over time using rate() or count_over_time().

            Useful for identifying traffic patterns, spikes, and anomalies.

            Args:
                query: Base LogQL selector (will be wrapped in rate or count_over_time)
                    Examples:
                    - '{namespace="production"}'
                    - '{app="api",status="error"}'
                start: Start timestamp
                end: End timestamp
                step: Query resolution (e.g., "1m", "5m", "15m")
                limit: Maximum data points to return

            Returns:
                Log volume metrics over time.

            Example:
                query_log_volume(
                    query='{namespace="production"}',
                    start="now-6h",
                    end="now",
                    step="5m"
                )
            """
            # Build a rate query
            metric_query = f"sum(rate({query}[5m])) by (app)"

            params = {
                "query": metric_query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "step": step,
                "limit": limit,
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        # ============================================================
        # ERROR & INCIDENT INVESTIGATION TOOLS (Epic 5)
        # ============================================================

        @self.mcp.tool()
        def find_error_patterns(
            namespace: str | None = None,
            service: str | None = None,
            start: str = "now-1h",
            end: str = "now",
            limit: int = 100,
        ) -> str:
            """
            Find common error patterns in logs.

            Searches for logs containing error indicators (error, exception, fatal, panic, fail)
            and returns them for pattern analysis.

            Args:
                namespace: Filter by Kubernetes namespace (optional)
                service: Filter by service/app name (optional)
                start: Start timestamp (default: now-1h)
                end: End timestamp (default: now)
                limit: Maximum number of entries (default: 100)

            Returns:
                Error logs with their patterns and frequencies.

            Example:
                find_error_patterns(
                    namespace="production",
                    service="api",
                    start="2024-01-15T00:00:00Z",
                    end="2024-01-15T23:59:59Z",
                    limit=50
                )
            """
            query = build_error_query(namespace, service)

            params = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "limit": limit,
                "direction": "backward",
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def get_error_spike_timeline(
            namespace: str | None = None,
            service: str | None = None,
            start: str = "now-6h",
            end: str = "now",
            step: str = "1m",
        ) -> str:
            """
            Visualize error spike timeline.

            Calculates error rate over time to identify when incidents started.

            Args:
                namespace: Filter by Kubernetes namespace (optional)
                service: Filter by service/app name (optional)
                start: Start timestamp (default: now-6h)
                end: End timestamp (default: now)
                step: Time resolution (default: 1m)

            Returns:
                Error rate timeline with spike indicators.

            Example:
                get_error_spike_timeline(
                    namespace="production",
                    service="api",
                    start="now-6h",
                    end="now",
                    step="1m"
                )
            """
            error_query = build_error_query(namespace, service)
            metric_query = f"sum(count_over_time({error_query}[{step}])) by (app)"

            params = {
                "query": metric_query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "step": step,
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def get_surrounding_logs(
            labels: dict[str, str],
            timestamp: str,
            before_lines: int = 50,
            after_lines: int = 50,
        ) -> str:
            """
            Retrieve logs before and after a specific timestamp.

            Useful for understanding the context around an error or event.

            Args:
                labels: Label selectors to identify the log stream.
                    Example: {"namespace": "prod", "pod": "api-123", "container": "app"}
                timestamp: Target timestamp (Unix nanoseconds or RFC3339)
                before_lines: Number of log lines before the timestamp (default: 50)
                after_lines: Number of log lines after the timestamp (default: 50)

            Returns:
                Log entries before and after the timestamp.

            Example:
                get_surrounding_logs(
                    labels={"namespace": "prod", "pod": "api-123"},
                    timestamp="2024-01-15T10:30:45.123Z",
                    before_lines=50,
                    after_lines=50
                )
            """
            # Convert timestamp to nanoseconds if needed
            ts = parse_time(timestamp)
            if not ts:
                return json.dumps({"error": "Invalid timestamp format"}, indent=2)

            # Calculate time range (approximate - using lines as seconds for simplicity)
            query, start_time, end_time = build_context_query(
                labels=labels,
                timestamp=ts,
                before_seconds=before_lines,
                after_seconds=after_lines,
            )

            params = {
                "query": query,
                "start": start_time,
                "end": end_time,
                "limit": before_lines + after_lines,
                "direction": "forward",
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        @self.mcp.tool()
        def trace_logs(
            trace_id: str,
            start: str = "now-1h",
            end: str = "now",
            limit: int = 1000,
        ) -> str:
            """
            Find all logs related to a trace ID.

            Correlates logs with distributed traces by searching for trace IDs.
            Supports various trace ID formats (hex, UUID, etc.).

            Args:
                trace_id: Trace ID to search for
                start: Start timestamp (default: now-1h)
                end: End timestamp (default: now)
                limit: Maximum number of entries (default: 1000)

            Returns:
                All logs for the trace, sorted chronologically.

            Example:
                trace_logs(
                    trace_id="abc123def456",
                    start="2024-01-15T10:00:00Z",
                    end="2024-01-15T11:00:00Z"
                )
            """
            query = build_trace_query(trace_id)

            params = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "limit": limit,
                "direction": "forward",  # Chronological order for traces
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        # ============================================================
        # MULTI-POD/CONTAINER ANALYSIS TOOLS (Epic 6)
        # ============================================================

        @self.mcp.tool()
        def find_pod_logs(
            pod_pattern: str,
            namespace: str,
            container: str | None = None,
            start: str = "now-1h",
            end: str = "now",
            limit: int = 1000,
        ) -> str:
            """
            Retrieve logs from pods matching a pattern.

            Useful for analyzing logs across all replicas of a deployment.

            Args:
                pod_pattern: Pod name pattern (supports wildcards with regex).
                    Examples:
                    - "api-.*" - All pods starting with "api-"
                    - "web-[0-9]+" - Web pods with numbers
                namespace: Kubernetes namespace
                container: Container name filter (optional)
                start: Start timestamp (default: now-1h)
                end: End timestamp (default: now)
                limit: Maximum number of entries (default: 1000)

            Returns:
                Aggregated logs from all matching pods.

            Example:
                find_pod_logs(
                    pod_pattern="api-.*",
                    namespace="production",
                    container="app",
                    start="2024-01-15T10:00:00Z",
                    end="2024-01-15T11:00:00Z"
                )
            """
            # Build query with regex pod matcher
            query = f'{{namespace="{namespace}",pod=~"{pod_pattern}"}}'
            if container:
                query = f'{{namespace="{namespace}",pod=~"{pod_pattern}",container="{container}"}}'

            params = {
                "query": query,
                "start": parse_time(start) or start,
                "end": parse_time(end) or end,
                "limit": limit,
                "direction": "forward",
            }

            with self._get_client() as client:
                response = client.get("/loki/api/v1/query_range", params=params)
                return self._format_response(response)

        # ============================================================
        # HEALTH & STATUS TOOLS (Epic 8)
        # ============================================================

        @self.mcp.tool()
        def check_loki_ready() -> str:
            """
            Check if Loki is ready to serve queries.

            Returns:
                Readiness status.

            Example:
                check_loki_ready()
            """
            with self._get_client() as client:
                response = client.get("/ready")
                if response.status_code == 200:
                    return json.dumps({"status": "ready"}, indent=2)
                else:
                    return json.dumps(
                        {"status": "not_ready", "error": response.error}, indent=2
                    )

        @self.mcp.tool()
        def get_loki_metrics() -> str:
            """
            Get Loki internal metrics (Prometheus format).

            Returns basic Loki server metrics for monitoring.

            Returns:
                Loki metrics in Prometheus exposition format.

            Example:
                get_loki_metrics()
            """
            with self._get_client() as client:
                response = client.get("/metrics")
                if response.success:
                    return json.dumps({"metrics": "available", "status_code": 200}, indent=2)
                else:
                    return self._format_response(response)
