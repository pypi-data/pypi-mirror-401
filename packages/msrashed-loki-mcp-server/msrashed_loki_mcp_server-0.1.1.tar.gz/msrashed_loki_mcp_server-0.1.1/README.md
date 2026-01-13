# Loki MCP Server

A read-only Model Context Protocol (MCP) server for Grafana Loki log aggregation platform. This server enables AI agents like Claude to query, search, and analyze logs from Loki for troubleshooting, incident investigation, and log analysis.

## Features

### Core Capabilities
- **Log Querying**: Execute LogQL instant and range queries
- **Label Discovery**: Explore available labels and their values
- **Series Discovery**: Find log streams matching label selectors
- **Error Analysis**: Detect error patterns and spike timelines
- **Incident Investigation**: Get surrounding context, trace logs, correlate events
- **Multi-Pod Analysis**: Aggregate logs across deployment replicas
- **Log Volume Metrics**: Analyze traffic patterns and anomalies

### Safety & Security
- **Read-only**: All operations are safe and cannot modify Loki
- **Authentication**: Supports Bearer token and Basic auth
- **Multi-tenancy**: X-Scope-OrgID header support for multi-tenant Loki
- **SSL Verification**: Configurable SSL certificate verification

## Installation

### Using uv (Recommended)

```bash
# Install from local directory
cd loki-mcp-server
uv pip install -e .

# Or install directly
uv pip install loki-mcp-server
```

### Using pip

```bash
pip install loki-mcp-server
```

## Configuration

### Environment Variables

```bash
# Required
export LOKI_URL="https://loki.example.com"

# Optional Authentication
export LOKI_TOKEN="your_bearer_token"
# OR
export LOKI_USERNAME="admin"
export LOKI_PASSWORD="secret"

# Optional Multi-tenancy
export LOKI_ORG_ID="tenant1"
# OR
export X_SCOPE_ORGID="tenant1"

# Optional Settings
export LOKI_TIMEOUT="30"           # Request timeout in seconds
export LOKI_VERIFY_SSL="true"      # Verify SSL certificates
```

### Running the Server

```bash
# Run with environment variables
loki-mcp-server

# Run with command-line arguments
loki-mcp-server --url https://loki.example.com --token your_token

# Run with HTTP transport
loki-mcp-server --transport http --port 8000

# Run with multi-tenancy
loki-mcp-server --url https://loki.example.com --org-id tenant1
```

### Command-Line Options

```
--url URL              Loki server URL
--token TOKEN          Bearer token for authentication
--username USER        Username for basic auth
--password PASS        Password for basic auth
--org-id ID            Organization ID for multi-tenancy
--timeout SECONDS      Request timeout (default: 30)
--no-verify-ssl        Disable SSL certificate verification
--transport TYPE       Transport: stdio, http, sse (default: stdio)
--host HOST            Host for HTTP/SSE transport (default: 127.0.0.1)
--port PORT            Port for HTTP/SSE transport (default: 8000)
```

## Available Tools

### Core Query Tools

#### `query_logs`
Execute LogQL instant query at a specific point in time.

```python
query_logs(
    query='{namespace="production",app="api"} |= "error" | json',
    limit=100,
    time="2024-01-15T10:00:00Z"
)
```

#### `query_logs_range`
Execute LogQL query over a time range.

```python
query_logs_range(
    query='{job="api-server"} |= "error"',
    start="2024-01-15T09:00:00Z",
    end="2024-01-15T10:00:00Z",
    limit=1000,
    direction="backward"
)
```

#### `query_log_volume`
Query log volume metrics over time.

```python
query_log_volume(
    query='{namespace="production"}',
    start="now-6h",
    end="now",
    step="5m"
)
```

### Label & Series Discovery

#### `list_labels`
List all available label names.

```python
list_labels(
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z"
)
```

#### `get_label_values`
Get all values for a specific label.

```python
get_label_values(
    label="namespace",
    start="2024-01-15T00:00:00Z"
)
```

#### `find_series`
Find log series matching label selectors.

```python
find_series(
    match=['{namespace="production"}', '{job="api"}'],
    start="2024-01-15T00:00:00Z"
)
```

### Metrics & Statistics

#### `get_index_stats`
Get index statistics for a query.

```python
get_index_stats(
    query='{namespace="production"}',
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z"
)
```

### Error & Incident Investigation

#### `find_error_patterns`
Find common error patterns in logs.

```python
find_error_patterns(
    namespace="production",
    service="api",
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z",
    limit=50
)
```

#### `get_error_spike_timeline`
Visualize error rate timeline.

```python
get_error_spike_timeline(
    namespace="production",
    service="api",
    start="now-6h",
    end="now",
    step="1m"
)
```

#### `get_surrounding_logs`
Get logs before and after a specific timestamp.

```python
get_surrounding_logs(
    labels={"namespace": "prod", "pod": "api-123"},
    timestamp="2024-01-15T10:30:45.123Z",
    before_lines=50,
    after_lines=50
)
```

#### `trace_logs`
Find all logs related to a trace ID.

```python
trace_logs(
    trace_id="abc123def456",
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T11:00:00Z"
)
```

### Multi-Pod Analysis

#### `find_pod_logs`
Retrieve logs from pods matching a pattern.

```python
find_pod_logs(
    pod_pattern="api-.*",
    namespace="production",
    container="app",
    start="2024-01-15T10:00:00Z",
    limit=1000
)
```

### Health & Status

#### `check_loki_ready`
Check if Loki is ready to serve queries.

```python
check_loki_ready()
```

#### `get_loki_metrics`
Get Loki internal metrics.

```python
get_loki_metrics()
```

## LogQL Query Syntax

### Basic Stream Selection
```logql
{namespace="production", app="api"}
```

### Filter by Text
```logql
{job="api-server"} |= "error" != "timeout"
```

### Parse JSON
```logql
{app="api"} | json | level="error"
```

### Parse Logfmt
```logql
{job="nginx"} | logfmt | status>=500
```

### Extract Fields
```logql
{app="api"} | json | line_format "{{.method}} {{.path}}"
```

### Metrics Queries
```logql
rate({namespace="production"}[5m])
sum(rate({app="api"}[1m])) by (status_code)
count_over_time({job="api"}[10m])
```

### Pattern Matching
```logql
{app="api"} |~ "error.*database"
{job="nginx"} | regexp "(?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+)"
```

## Usage Examples

### Example 1: Find Recent Errors

```python
# Find errors in the last hour
find_error_patterns(
    namespace="production",
    service="api",
    start="now-1h",
    end="now",
    limit=100
)
```

### Example 2: Investigate Error Spike

```python
# Step 1: Get error timeline to identify spike
get_error_spike_timeline(
    namespace="production",
    service="api",
    start="now-6h",
    end="now",
    step="1m"
)

# Step 2: Query logs during spike period
query_logs_range(
    query='{namespace="production",app="api"} |= "error"',
    start="2024-01-15T10:25:00Z",
    end="2024-01-15T10:35:00Z",
    limit=500
)

# Step 3: Get context around specific error
get_surrounding_logs(
    labels={"namespace": "production", "pod": "api-xyz"},
    timestamp="2024-01-15T10:30:45.123Z",
    before_lines=50,
    after_lines=50
)
```

### Example 3: Trace Request Across Services

```python
# Find all logs for a trace ID
trace_logs(
    trace_id="a1b2c3d4e5f6",
    start="now-1h",
    end="now"
)
```

### Example 4: Analyze All Replicas

```python
# Get logs from all API pods
find_pod_logs(
    pod_pattern="api-.*",
    namespace="production",
    container="app",
    start="now-1h",
    end="now"
)
```

### Example 5: Monitor Log Volume

```python
# Query log volume by service
query_log_volume(
    query='{namespace="production"}',
    start="now-24h",
    end="now",
    step="15m"
)
```

## Use Cases

### Troubleshooting Production Issues
1. Detect error patterns across services
2. Identify when errors started (spike timeline)
3. Get context around specific errors
4. Correlate logs with traces

### Performance Investigation
1. Analyze log volume patterns
2. Identify traffic spikes
3. Compare log rates across services
4. Monitor query performance

### Incident Response
1. Quick error pattern discovery
2. Multi-pod log aggregation
3. Timeline reconstruction
4. Root cause analysis with context

### Debugging
1. Find logs for specific trace IDs
2. Get surrounding context logs
3. Parse structured JSON/logfmt logs
4. Filter by custom fields

## Integration with Claude Code

Add to your Claude Code MCP settings (`~/.claude/mcp_settings.json`):

```json
{
  "mcpServers": {
    "loki": {
      "command": "loki-mcp-server",
      "env": {
        "LOKI_URL": "https://loki.example.com",
        "LOKI_TOKEN": "your_token_here",
        "LOKI_ORG_ID": "tenant1"
      }
    }
  }
}
```

Or with basic auth:

```json
{
  "mcpServers": {
    "loki": {
      "command": "loki-mcp-server",
      "env": {
        "LOKI_URL": "https://loki.example.com",
        "LOKI_USERNAME": "admin",
        "LOKI_PASSWORD": "secret"
      }
    }
  }
}
```

## Architecture

### Technology Stack
- **Framework**: FastMCP 2.0
- **HTTP Client**: httpx (with connection pooling)
- **Python**: 3.12+
- **Type Hints**: Full type coverage
- **Time Parsing**: python-dateutil

### Project Structure
```
loki-mcp-server/
├── pyproject.toml
├── README.md
├── USER_STORIES.md
└── src/
    └── loki_mcp_server/
        ├── __init__.py
        ├── __main__.py
        ├── server.py           # FastMCP server setup
        ├── tools/
        │   ├── __init__.py
        │   └── registry.py     # All tool implementations
        └── utils/
            ├── __init__.py
            ├── client.py       # Loki HTTP client
            ├── logql.py        # LogQL helpers
            └── time.py         # Time parsing utilities
```

## Authentication Methods

### 1. Bearer Token
```bash
export LOKI_TOKEN="your_bearer_token"
loki-mcp-server
```

### 2. Basic Authentication
```bash
export LOKI_USERNAME="admin"
export LOKI_PASSWORD="secret"
loki-mcp-server
```

### 3. No Authentication
```bash
export LOKI_URL="http://localhost:3100"
loki-mcp-server
```

## Multi-Tenancy

For multi-tenant Loki installations, set the organization ID:

```bash
export LOKI_ORG_ID="tenant1"
# OR
export X_SCOPE_ORGID="tenant1"

loki-mcp-server
```

This adds the `X-Scope-OrgID` header to all requests, required by multi-tenant Loki.

## Time Formats

The server supports multiple time formats:

### RFC3339
```
2024-01-15T10:00:00Z
2024-01-15T10:00:00-05:00
```

### Unix Timestamps
```
1705316400              (seconds)
1705316400000000000     (nanoseconds)
```

### Relative Times
```
now
now-1h
now-15m
now-6h
```

## Limitations

### Read-Only Operations
- No log ingestion (push) capabilities
- No configuration changes
- No deletion operations
- All write endpoints are blocked

### Query Limits
- Default limit: 100 entries for instant queries
- Default limit: 1000 entries for range queries
- Configurable via limit parameter
- Large result sets may be truncated

### Timeout
- Default timeout: 30 seconds
- Configurable via `--timeout` or `LOKI_TIMEOUT`
- Long-running queries may timeout

## Troubleshooting

### Connection Issues
```bash
# Test Loki connectivity
check_loki_ready()

# Check server metrics
get_loki_metrics()
```

### Authentication Errors
- Verify token/credentials are correct
- Check if authentication is required
- Ensure proper environment variables are set

### Multi-Tenancy Issues
- Verify org ID is correct
- Check if X-Scope-OrgID header is required
- Test with different tenant IDs

### Query Errors
- Validate LogQL syntax
- Check label selectors are correct
- Verify time range is valid
- Ensure labels exist in Loki

## Contributing

Contributions are welcome! Please ensure:
- Python 3.12+ compatibility
- Full type hints
- Comprehensive docstrings
- Read-only operations only

## License

MIT License - See LICENSE file for details

## References

- [Loki HTTP API Documentation](https://grafana.com/docs/loki/latest/reference/loki-http-api/)
- [LogQL Documentation](https://grafana.com/docs/loki/latest/query/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Support

For issues, questions, or contributions:
- GitHub Issues: [Create an issue]
- Documentation: [Loki Docs](https://grafana.com/docs/loki/)
- MCP Discord: [Join the community]
