"""
Loki MCP Server.

A read-only MCP server for Grafana Loki log aggregation platform.
All operations are safe and cannot modify Loki configuration.
"""

from mcp.server.fastmcp import FastMCP

from loki_mcp_server.tools import LokiTools

SERVER_INSTRUCTIONS = """
Loki MCP Server - Read-Only Log Querying & Analysis

This server provides read-only access to Grafana Loki log aggregation system.
All operations are safe and cannot modify your Loki configuration.

## Available Tools:

### Core Query Tools
- **query_logs**: Execute LogQL instant queries at a specific point in time
- **query_logs_range**: Execute LogQL queries over a time range
- **query_log_volume**: Query log volume metrics over time (rate/count)

### Label & Series Discovery
- **list_labels**: List all available label names
- **get_label_values**: Get all values for a specific label
- **find_series**: Find log series matching label selectors

### Metrics & Statistics
- **get_index_stats**: Get index statistics (chunks, streams, bytes, entries)
- **query_log_volume**: Query log volume and identify traffic patterns

### Error & Incident Investigation
- **find_error_patterns**: Find common error patterns in logs
- **get_error_spike_timeline**: Visualize error rate timeline with spikes
- **get_surrounding_logs**: Get logs before and after a specific timestamp
- **trace_logs**: Find all logs related to a trace ID

### Multi-Pod Analysis
- **find_pod_logs**: Retrieve logs from pods matching a pattern (all replicas)

### Health & Status
- **check_loki_ready**: Check if Loki is ready to serve queries
- **get_loki_metrics**: Get Loki internal metrics

## LogQL Query Syntax:

### Basic Stream Selection
```
{namespace="production", app="api"}
```

### Filter by Text
```
{job="api-server"} |= "error" != "timeout"
```

### Parse JSON
```
{app="api"} | json | level="error"
```

### Parse Logfmt
```
{job="nginx"} | logfmt | status>=500
```

### Extract Fields
```
{app="api"} | json | line_format "{{.method}} {{.path}}"
```

### Metrics Queries
```
rate({namespace="production"}[5m])
sum(rate({app="api"}[1m])) by (status_code)
count_over_time({job="api"}[10m])
```

### Pattern Matching
```
{app="api"} |~ "error.*database"
{job="nginx"} | regexp "(?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+)"
```

## Common Use Cases:

### Find Recent Errors
```
find_error_patterns(
    namespace="production",
    service="api",
    start="now-1h",
    end="now"
)
```

### Investigate Incident Timeline
```
get_error_spike_timeline(
    namespace="production",
    service="api",
    start="now-6h",
    end="now",
    step="1m"
)
```

### Get Context Around Error
```
get_surrounding_logs(
    labels={"namespace": "prod", "pod": "api-123"},
    timestamp="2024-01-15T10:30:45.123Z",
    before_lines=50,
    after_lines=50
)
```

### Trace Request Across Services
```
trace_logs(
    trace_id="abc123def456",
    start="now-1h",
    end="now"
)
```

### Analyze All Replicas
```
find_pod_logs(
    pod_pattern="api-.*",
    namespace="production",
    container="app",
    start="now-1h",
    end="now"
)
```

## Authentication:
Set environment variables:
- LOKI_URL: Loki server URL
- LOKI_TOKEN: Bearer token (optional)
- LOKI_USERNAME/LOKI_PASSWORD: Basic auth (optional)
- LOKI_ORG_ID or X_SCOPE_ORGID: Multi-tenant organization ID (optional)

## Multi-Tenancy:
For multi-tenant Loki installations, set the organization ID:
- LOKI_ORG_ID environment variable
- Or pass org_id parameter when creating the server

This adds the X-Scope-OrgID header to all requests.

## Safety:
- All operations are READ-ONLY
- Write operations (push logs, delete) are blocked
- Uses your Loki credentials for authentication
"""


def create_server(
    url: str | None = None,
    token: str | None = None,
    username: str | None = None,
    password: str | None = None,
    org_id: str | None = None,
    timeout: int = 30,
    verify_ssl: bool = True,
) -> FastMCP:
    """
    Create and configure the Loki MCP server.

    Args:
        url: Loki server URL (or use LOKI_URL env var)
        token: Bearer token for authentication (optional)
        username: Username for basic auth (optional)
        password: Password for basic auth (optional)
        org_id: Organization ID for multi-tenancy (X-Scope-OrgID header)
        timeout: Request timeout in seconds
        verify_ssl: Verify SSL certificates

    Returns:
        Configured FastMCP server instance
    """
    mcp = FastMCP(
        name="loki-mcp-server",
        instructions=SERVER_INSTRUCTIONS,
    )

    # Register all Loki tools
    LokiTools(
        mcp=mcp,
        url=url,
        token=token,
        username=username,
        password=password,
        org_id=org_id,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )

    return mcp


def main() -> None:
    """Entry point for the Loki MCP server."""
    from loki_mcp_server.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
