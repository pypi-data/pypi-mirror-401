"""
Command-line interface for Loki MCP Server.

Provides a Click-based CLI for running the MCP server and testing
all Loki tools directly from the command line.
"""

import json
import sys
from collections.abc import Callable
from functools import wraps
from typing import Any

import click

from loki_mcp_server.server import create_server
from loki_mcp_server.utils.client import LokiClient
from loki_mcp_server.utils.time import parse_time


def common_options(func: Callable) -> Callable:
    """Decorator to add common Loki connection options."""

    @click.option(
        "--url",
        envvar=["LOKI_URL"],
        default="http://localhost:3100",
        help="Loki server URL.",
        show_envvar=True,
    )
    @click.option(
        "--token",
        envvar=["LOKI_TOKEN"],
        default=None,
        help="Bearer token for authentication.",
        show_envvar=True,
    )
    @click.option(
        "--username",
        envvar="LOKI_USERNAME",
        default=None,
        help="Username for basic auth.",
        show_envvar=True,
    )
    @click.option(
        "--password",
        envvar="LOKI_PASSWORD",
        default=None,
        help="Password for basic auth.",
        show_envvar=True,
    )
    @click.option(
        "--org-id",
        envvar=["LOKI_ORG_ID", "X_SCOPE_ORGID"],
        default=None,
        help="Organization ID for multi-tenancy (X-Scope-OrgID header).",
        show_envvar=True,
    )
    @click.option(
        "--timeout",
        envvar="LOKI_TIMEOUT",
        type=int,
        default=30,
        help="Request timeout in seconds.",
        show_default=True,
    )
    @click.option(
        "--verify-ssl/--no-verify-ssl",
        envvar="LOKI_VERIFY_SSL",
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
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
) -> LokiClient:
    """Create a Loki client with the given options."""
    return LokiClient(
        url=url,
        token=token,
        username=username,
        password=password,
        org_id=org_id,
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
@click.version_option(package_name="loki-mcp-server")
def cli() -> None:
    """Loki MCP Server - Read-only log querying and analysis.

    A Model Context Protocol (MCP) server that provides read-only access
    to Grafana Loki log aggregation platform.

    \b
    Commands are organized into groups:
      run       Start the MCP server
      query     Execute LogQL queries
      labels    Discover labels and series
      analyze   Error patterns and investigation tools
      status    Check server status
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
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    transport: str,
    host: str,
    port: int,
) -> None:
    """Run the Loki MCP server.

    \b
    Examples:
      # Run with stdio transport (default)
      loki-mcp-server run

      # Run with HTTP transport
      loki-mcp-server run --transport http --port 8000

      # Run with custom Loki URL
      loki-mcp-server run --url https://loki.example.com

      # Run with multi-tenancy
      loki-mcp-server run --org-id tenant1
    """
    server = create_server(
        url=url,
        token=token,
        username=username,
        password=password,
        org_id=org_id,
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
    """Execute LogQL queries.

    \b
    Available commands:
      instant    Execute instant query at a single point in time
      range      Execute range query over a time period
      volume     Query log volume metrics
    """
    pass


@query.command("instant")
@common_options
@click.argument("logql")
@click.option(
    "--time", "-t",
    default=None,
    help="Evaluation timestamp (RFC3339, Unix, or 'now', 'now-1h').",
)
@click.option(
    "--limit", "-l",
    type=int,
    default=100,
    help="Maximum number of entries to return.",
    show_default=True,
)
@click.option(
    "--direction",
    type=click.Choice(["forward", "backward"]),
    default="backward",
    help="Return direction.",
    show_default=True,
)
def query_instant(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    logql: str,
    time: str | None,
    limit: int,
    direction: str,
) -> None:
    """Execute a LogQL instant query.

    \b
    Examples:
      # Basic log query
      loki-mcp-server query instant '{namespace="production"}'

      # Query with text filter
      loki-mcp-server query instant '{job="api"} |= "error"'

      # Query at specific time
      loki-mcp-server query instant '{app="api"}' --time "now-1h"

      # Query with JSON parsing
      loki-mcp-server query instant '{app="api"} | json | level="error"'
    """
    params: dict[str, Any] = {
        "query": logql,
        "limit": limit,
        "direction": direction,
    }

    if time:
        parsed_time = parse_time(time)
        if parsed_time:
            params["time"] = parsed_time

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query", params=params)
        output_response(response)


@query.command("range")
@common_options
@click.argument("logql")
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
    "--limit", "-l",
    type=int,
    default=1000,
    help="Maximum number of entries to return.",
    show_default=True,
)
@click.option(
    "--step",
    default=None,
    help="Query resolution for metric queries (e.g., '15s', '1m').",
)
@click.option(
    "--direction",
    type=click.Choice(["forward", "backward"]),
    default="backward",
    help="Return direction.",
    show_default=True,
)
def query_range(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    logql: str,
    start: str,
    end: str,
    limit: int,
    step: str | None,
    direction: str,
) -> None:
    """Execute a LogQL range query over a time period.

    \b
    Examples:
      # Logs over last hour
      loki-mcp-server query range '{job="api"} |= "error"' \\
          --start now-1h --end now

      # Metric query with step
      loki-mcp-server query range 'rate({namespace="prod"}[5m])' \\
          --start now-6h --end now --step 1m
    """
    params: dict[str, Any] = {
        "query": logql,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
        "limit": limit,
        "direction": direction,
    }

    if step:
        params["step"] = step

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


@query.command("volume")
@common_options
@click.argument("logql")
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
@click.option(
    "--step",
    default="5m",
    help="Query resolution (e.g., '1m', '5m', '15m').",
    show_default=True,
)
def query_volume(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    logql: str,
    start: str,
    end: str,
    step: str,
) -> None:
    """Query log volume over time.

    \b
    Examples:
      # Volume by app
      loki-mcp-server query volume '{namespace="production"}' \\
          --start now-6h --end now --step 5m
    """
    metric_query = f"sum(rate({logql}[5m])) by (app)"

    params = {
        "query": metric_query,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
        "step": step,
    }

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


# ============================================================
# Labels Commands Group
# ============================================================


@cli.group()
def labels() -> None:
    """Discover labels, values, and series.

    \b
    Available commands:
      list         List all label names
      values       Get values for a label
      series       Find matching log series
    """
    pass


@labels.command("list")
@common_options
@click.option("--start", "-s", default=None, help="Start timestamp.")
@click.option("--end", "-e", default=None, help="End timestamp.")
def list_labels(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    start: str | None,
    end: str | None,
) -> None:
    """List all available label names.

    \b
    Examples:
      # List all labels
      loki-mcp-server labels list

      # List labels for a time range
      loki-mcp-server labels list --start now-24h --end now
    """
    params = {}
    if start:
        params["start"] = parse_time(start)
    if end:
        params["end"] = parse_time(end)

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/labels", params=params if params else None)
        output_response(response)


@labels.command("values")
@common_options
@click.argument("label")
@click.option("--start", "-s", default=None, help="Start timestamp.")
@click.option("--end", "-e", default=None, help="End timestamp.")
@click.option("--query", "-q", default=None, help="LogQL query to filter results.")
def get_label_values(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    label: str,
    start: str | None,
    end: str | None,
    query: str | None,
) -> None:
    """Get all values for a specific label.

    \b
    Examples:
      # Get all namespaces
      loki-mcp-server labels values namespace

      # Get apps in production
      loki-mcp-server labels values app --query '{namespace="production"}'
    """
    params = {}
    if start:
        params["start"] = parse_time(start)
    if end:
        params["end"] = parse_time(end)
    if query:
        params["query"] = query

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get(
            f"/loki/api/v1/label/{label}/values",
            params=params if params else None,
        )
        output_response(response)


@labels.command("series")
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
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    match: tuple[str, ...],
    start: str | None,
    end: str | None,
) -> None:
    """Find log series matching label selectors.

    \b
    Examples:
      # Find all series for a namespace
      loki-mcp-server labels series --match '{namespace="production"}'

      # Find multiple selectors
      loki-mcp-server labels series --match '{job="api"}' --match '{job="web"}'
    """
    params: dict[str, Any] = {"match[]": list(match)}
    if start:
        params["start"] = parse_time(start)
    if end:
        params["end"] = parse_time(end)

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/series", params=params)
        output_response(response)


# ============================================================
# Analyze Commands Group
# ============================================================


@cli.group()
def analyze() -> None:
    """Error patterns and investigation tools.

    \b
    Available commands:
      errors        Find common error patterns
      error-timeline  Visualize error rate over time
      context       Get logs around a timestamp
      trace         Find logs for a trace ID
      pods          Get logs from pods matching a pattern
    """
    pass


@analyze.command("errors")
@common_options
@click.option("--namespace", "-n", default=None, help="Kubernetes namespace.")
@click.option("--service", "-s", default=None, help="Service/app name.")
@click.option("--start", default="now-1h", help="Start timestamp.", show_default=True)
@click.option("--end", default="now", help="End timestamp.", show_default=True)
@click.option("--limit", "-l", type=int, default=100, help="Maximum entries.", show_default=True)
def find_errors(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    namespace: str | None,
    service: str | None,
    start: str,
    end: str,
    limit: int,
) -> None:
    """Find common error patterns in logs.

    \b
    Examples:
      # Find errors in production
      loki-mcp-server analyze errors --namespace production

      # Find errors for a specific service
      loki-mcp-server analyze errors --namespace prod --service api
    """
    from loki_mcp_server.utils.logql import build_error_query

    query = build_error_query(namespace, service)

    params = {
        "query": query,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
        "limit": limit,
        "direction": "backward",
    }

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


@analyze.command("error-timeline")
@common_options
@click.option("--namespace", "-n", default=None, help="Kubernetes namespace.")
@click.option("--service", "-s", default=None, help="Service/app name.")
@click.option("--start", default="now-6h", help="Start timestamp.", show_default=True)
@click.option("--end", default="now", help="End timestamp.", show_default=True)
@click.option("--step", default="1m", help="Time resolution.", show_default=True)
def error_timeline(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    namespace: str | None,
    service: str | None,
    start: str,
    end: str,
    step: str,
) -> None:
    """Visualize error rate timeline.

    \b
    Examples:
      # Error timeline for last 6 hours
      loki-mcp-server analyze error-timeline --namespace production

      # High resolution timeline
      loki-mcp-server analyze error-timeline --namespace prod --step 30s
    """
    from loki_mcp_server.utils.logql import build_error_query

    error_query = build_error_query(namespace, service)
    metric_query = f"sum(count_over_time({error_query}[{step}])) by (app)"

    params = {
        "query": metric_query,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
        "step": step,
    }

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


@analyze.command("context")
@common_options
@click.option(
    "--labels", "-l",
    required=True,
    help='Label selectors as JSON (e.g., \'{"namespace": "prod", "pod": "api-123"}\').',
)
@click.option(
    "--timestamp", "-t",
    required=True,
    help="Target timestamp (RFC3339 or Unix nanoseconds).",
)
@click.option("--before", type=int, default=50, help="Lines before timestamp.", show_default=True)
@click.option("--after", type=int, default=50, help="Lines after timestamp.", show_default=True)
def get_context(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    labels: str,
    timestamp: str,
    before: int,
    after: int,
) -> None:
    """Get logs around a specific timestamp.

    \b
    Examples:
      # Get context around an error
      loki-mcp-server analyze context \\
          --labels '{"namespace": "prod", "pod": "api-123"}' \\
          --timestamp "2024-01-15T10:30:45.123Z" \\
          --before 50 --after 50
    """
    from loki_mcp_server.utils.logql import build_context_query

    try:
        label_dict = json.loads(labels)
    except json.JSONDecodeError:
        click.echo(click.style("Error: Invalid JSON for labels", fg="red"), err=True)
        sys.exit(1)

    ts = parse_time(timestamp)
    if not ts:
        click.echo(click.style("Error: Invalid timestamp format", fg="red"), err=True)
        sys.exit(1)

    query, start_time, end_time = build_context_query(
        labels=label_dict,
        timestamp=ts,
        before_seconds=before,
        after_seconds=after,
    )

    params = {
        "query": query,
        "start": start_time,
        "end": end_time,
        "limit": before + after,
        "direction": "forward",
    }

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


@analyze.command("trace")
@common_options
@click.argument("trace_id")
@click.option("--start", default="now-1h", help="Start timestamp.", show_default=True)
@click.option("--end", default="now", help="End timestamp.", show_default=True)
@click.option("--limit", "-l", type=int, default=1000, help="Maximum entries.", show_default=True)
def trace_logs(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    trace_id: str,
    start: str,
    end: str,
    limit: int,
) -> None:
    """Find all logs related to a trace ID.

    \b
    Examples:
      # Find logs for a trace
      loki-mcp-server analyze trace abc123def456

      # With specific time range
      loki-mcp-server analyze trace abc123 --start now-2h --end now
    """
    from loki_mcp_server.utils.logql import build_trace_query

    query = build_trace_query(trace_id)

    params = {
        "query": query,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
        "limit": limit,
        "direction": "forward",
    }

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


@analyze.command("pods")
@common_options
@click.argument("pod_pattern")
@click.option("--namespace", "-n", required=True, help="Kubernetes namespace.")
@click.option("--container", "-c", default=None, help="Container name filter.")
@click.option("--start", default="now-1h", help="Start timestamp.", show_default=True)
@click.option("--end", default="now", help="End timestamp.", show_default=True)
@click.option("--limit", "-l", type=int, default=1000, help="Maximum entries.", show_default=True)
def find_pod_logs(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    pod_pattern: str,
    namespace: str,
    container: str | None,
    start: str,
    end: str,
    limit: int,
) -> None:
    """Get logs from pods matching a pattern.

    \b
    Examples:
      # All API pods
      loki-mcp-server analyze pods "api-.*" --namespace production

      # Specific container
      loki-mcp-server analyze pods "web-.*" --namespace prod --container app
    """
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

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/query_range", params=params)
        output_response(response)


# ============================================================
# Stats Commands Group
# ============================================================


@cli.group()
def stats() -> None:
    """Index statistics and metrics.

    \b
    Available commands:
      index     Get index statistics for a query
    """
    pass


@stats.command("index")
@common_options
@click.argument("logql")
@click.option("--start", "-s", required=True, help="Start timestamp.")
@click.option("--end", "-e", required=True, help="End timestamp.")
def index_stats(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
    logql: str,
    start: str,
    end: str,
) -> None:
    """Get index statistics for a query.

    \b
    Examples:
      loki-mcp-server stats index '{namespace="production"}' \\
          --start now-24h --end now
    """
    params = {
        "query": logql,
        "start": parse_time(start) or start,
        "end": parse_time(end) or end,
    }

    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/loki/api/v1/index/stats", params=params)
        output_response(response)


# ============================================================
# Status Commands Group
# ============================================================


@cli.group()
def status() -> None:
    """Check server status.

    \b
    Available commands:
      ready      Check if Loki is ready
      metrics    Get Loki internal metrics
    """
    pass


@status.command("ready")
@common_options
def check_ready(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Check if Loki is ready to serve queries.

    \b
    Examples:
      loki-mcp-server status ready
    """
    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/ready")
        if response.status_code == 200:
            click.echo(json.dumps({"status": "ready"}, indent=2))
        else:
            click.echo(json.dumps({"status": "not_ready", "error": response.error}, indent=2))
            sys.exit(1)


@status.command("metrics")
@common_options
def get_metrics(
    url: str,
    token: str | None,
    username: str | None,
    password: str | None,
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Get Loki internal metrics.

    \b
    Examples:
      loki-mcp-server status metrics
    """
    with get_client(url, token, username, password, org_id, timeout, verify_ssl) as client:
        response = client.get("/metrics")
        if response.success or response.status_code == 200:
            click.echo(json.dumps({"status": "available", "metrics": "ok"}, indent=2))
        else:
            click.echo(
                click.style(f"Error: {response.error}", fg="red"),
                err=True,
            )
            sys.exit(1)


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
    org_id: str | None,
    timeout: int,
    verify_ssl: bool,
) -> None:
    """Check connection to Loki server.

    Verifies connectivity and authentication.

    \b
    Examples:
      loki-mcp-server check
      loki-mcp-server check --url https://loki.example.com
    """
    click.echo(f"Checking connection to {url}...")

    client = get_client(url, token, username, password, org_id, timeout, verify_ssl)

    try:
        # Check readiness endpoint
        response = client.get("/ready")
        if response.status_code == 200:
            click.echo(click.style("  Readiness check: OK", fg="green"))
        else:
            click.echo(click.style(f"  Readiness check: FAILED ({response.error})", fg="red"))

        # Check labels endpoint (basic API test)
        response = client.get("/loki/api/v1/labels")
        if response.success:
            label_count = len(response.data) if response.data else 0
            click.echo(click.style(f"  API check: OK ({label_count} labels found)", fg="green"))
            click.echo(click.style("\nConnection successful!", fg="green", bold=True))
        else:
            click.echo(click.style(f"  API check: FAILED ({response.error})", fg="red"))

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
    click.echo("Loki MCP Server - Tools & CLI Commands\n")
    click.echo("=" * 60)

    mappings = [
        ("Query Tools", [
            ("query_logs", "query instant", "Instant LogQL query"),
            ("query_logs_range", "query range", "Range LogQL query"),
            ("query_log_volume", "query volume", "Log volume metrics"),
        ]),
        ("Label Discovery", [
            ("list_labels", "labels list", "List label names"),
            ("get_label_values", "labels values", "Get label values"),
            ("find_series", "labels series", "Find log series"),
        ]),
        ("Analysis Tools", [
            ("find_error_patterns", "analyze errors", "Find error patterns"),
            ("get_error_spike_timeline", "analyze error-timeline", "Error rate timeline"),
            ("get_surrounding_logs", "analyze context", "Get context logs"),
            ("trace_logs", "analyze trace", "Trace correlation"),
            ("find_pod_logs", "analyze pods", "Multi-pod logs"),
        ]),
        ("Statistics", [
            ("get_index_stats", "stats index", "Index statistics"),
        ]),
        ("Status", [
            ("check_loki_ready", "status ready", "Check readiness"),
            ("get_loki_metrics", "status metrics", "Get metrics"),
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
    click.echo("\nRun 'loki-mcp-server <command> --help' for details.")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
