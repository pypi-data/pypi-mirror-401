# Loki MCP Server - Quick Start Guide

Get started with the Loki MCP Server in 5 minutes.

## 1. Installation

```bash
cd loki-mcp-server
uv pip install -e .
```

## 2. Configuration

### Option A: Local Loki (No Auth)

```bash
export LOKI_URL="http://localhost:3100"
loki-mcp-server
```

### Option B: Remote Loki with Token

```bash
export LOKI_URL="https://loki.example.com"
export LOKI_TOKEN="your_bearer_token"
loki-mcp-server
```

### Option C: Multi-Tenant Loki

```bash
export LOKI_URL="https://loki.example.com"
export LOKI_TOKEN="your_bearer_token"
export LOKI_ORG_ID="tenant1"
loki-mcp-server
```

## 3. Integrate with Claude Code

Add to `~/.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "loki": {
      "command": "loki-mcp-server",
      "env": {
        "LOKI_URL": "http://localhost:3100"
      }
    }
  }
}
```

## 4. Common Use Cases

### Find Recent Errors

Ask Claude:
> "Using the loki MCP server, find all errors in the production namespace from the last hour"

Claude will execute:
```python
find_error_patterns(
    namespace="production",
    start="now-1h",
    end="now"
)
```

### Investigate Error Spike

Ask Claude:
> "Show me the error timeline for the API service over the last 6 hours"

Claude will execute:
```python
get_error_spike_timeline(
    service="api",
    start="now-6h",
    end="now",
    step="1m"
)
```

### Get Context Around Error

Ask Claude:
> "Get 50 log lines before and after this timestamp: 2024-01-15T10:30:45Z for pod api-xyz in production"

Claude will execute:
```python
get_surrounding_logs(
    labels={"namespace": "production", "pod": "api-xyz"},
    timestamp="2024-01-15T10:30:45.123Z",
    before_lines=50,
    after_lines=50
)
```

### Trace Request Logs

Ask Claude:
> "Find all logs for trace ID abc123def456"

Claude will execute:
```python
trace_logs(
    trace_id="abc123def456",
    start="now-1h",
    end="now"
)
```

### Analyze All Replicas

Ask Claude:
> "Show me logs from all API pods in the last hour"

Claude will execute:
```python
find_pod_logs(
    pod_pattern="api-.*",
    namespace="production",
    start="now-1h",
    end="now"
)
```

## 5. Available Tools

- `query_logs` - Query logs at a point in time
- `query_logs_range` - Query logs over a time range
- `query_log_volume` - Analyze log volume metrics
- `list_labels` - Discover available labels
- `get_label_values` - Get values for a label
- `find_series` - Find log streams
- `get_index_stats` - Get index statistics
- `find_error_patterns` - Find error patterns
- `get_error_spike_timeline` - Error timeline
- `get_surrounding_logs` - Context logs
- `trace_logs` - Trace correlation
- `find_pod_logs` - Multi-pod analysis
- `check_loki_ready` - Health check
- `get_loki_metrics` - Server metrics

## 6. LogQL Query Examples

### Basic Queries
```logql
{namespace="production", app="api"}
{job="api-server"} |= "error"
{app="api"} | json | level="error"
```

### Metric Queries
```logql
rate({namespace="production"}[5m])
sum(rate({app="api"}[1m])) by (status_code)
count_over_time({job="api"}[10m])
```

## 7. Troubleshooting

### Test Connection
```bash
# Check if Loki is ready
curl $LOKI_URL/ready

# Or use the MCP tool
check_loki_ready()
```

### Authentication Issues
```bash
# Verify token
curl -H "Authorization: Bearer $LOKI_TOKEN" $LOKI_URL/loki/api/v1/labels

# Verify basic auth
curl -u $LOKI_USERNAME:$LOKI_PASSWORD $LOKI_URL/loki/api/v1/labels
```

### Multi-Tenancy Issues
```bash
# Verify org ID
curl -H "X-Scope-OrgID: $LOKI_ORG_ID" $LOKI_URL/loki/api/v1/labels
```

## 8. Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [USER_STORIES.md](USER_STORIES.md) for all supported features
- Explore the [Loki HTTP API docs](https://grafana.com/docs/loki/latest/reference/loki-http-api/)
- Learn [LogQL query syntax](https://grafana.com/docs/loki/latest/query/)

## Support

For issues or questions:
- Check the README troubleshooting section
- Review Loki documentation
- Create a GitHub issue
