# Loki MCP Server - User Stories

## Overview
Enable AI agents like Claude Code to query, search, and analyze logs from Grafana Loki for troubleshooting, incident investigation, and log analysis.

## Epic 1: Core Log Querying

### US-1.1: Execute LogQL Instant Queries
**As an** AI agent
**I want to** execute LogQL instant queries at a specific point in time
**So that** I can retrieve log entries for a specific moment

**Acceptance Criteria:**
- Support LogQL log stream selectors
- Support log pipeline operations
- Return log entries with labels and timestamps
- Limit results to prevent overwhelming responses
- Handle query errors gracefully

**API Endpoint:** `GET /loki/api/v1/query`

**Example Usage:**
```python
query_logs(
    query='{namespace="production",app="api"} |= "error" | json',
    limit=100,
    time="2024-01-15T10:00:00Z"
)
```

### US-1.2: Execute LogQL Range Queries
**As an** AI agent
**I want to** execute LogQL queries over a time range
**So that** I can analyze logs across a time period

**Acceptance Criteria:**
- Support start and end timestamps
- Support limit parameter for result size
- Support direction (forward/backward)
- Support step parameter for metrics
- Handle both log and metric queries
- Return structured log entries with metadata

**API Endpoint:** `GET /loki/api/v1/query_range`

**Example Usage:**
```python
query_logs_range(
    query='{job="api-server"} |= "error"',
    start="2024-01-15T09:00:00Z",
    end="2024-01-15T10:00:00Z",
    limit=1000,
    direction="backward"
)
```

### US-1.3: Tail Log Streams
**As an** AI agent
**I want to** tail log streams in real-time
**So that** I can monitor live log data

**Acceptance Criteria:**
- Support WebSocket streaming
- Follow log streams as new entries arrive
- Support delay_for parameter
- Limit stream rate
- Handle disconnections gracefully

**API Endpoint:** `GET /loki/api/v1/tail`

---

## Epic 2: Label & Stream Discovery

### US-2.1: List Label Names
**As an** AI agent
**I want to** list all available label names
**So that** I can discover what dimensions are available for filtering

**Acceptance Criteria:**
- Return all unique label names
- Support time range filtering
- Support query parameter for filtering
- Include common labels (job, namespace, pod, etc.)

**API Endpoint:** `GET /loki/api/v1/labels` or `GET /loki/api/v1/label`

**Example Usage:**
```python
query_labels(
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z"
)
```

### US-2.2: Get Label Values
**As an** AI agent
**I want to** retrieve all values for a specific label
**So that** I can filter logs by available label values

**Acceptance Criteria:**
- Return all unique values for a label
- Support time range filtering
- Support query parameter for additional filtering
- Handle high cardinality labels

**API Endpoint:** `GET /loki/api/v1/label/<label_name>/values`

**Example Usage:**
```python
query_label_values(
    label="namespace",
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z"
)
```

### US-2.3: Find Log Series
**As an** AI agent
**I want to** find all log series matching label selectors
**So that** I can discover available log streams

**Acceptance Criteria:**
- Support label matchers
- Return series label sets
- Support time range filtering
- Handle high cardinality

**API Endpoint:** `GET /loki/api/v1/series` or `POST /loki/api/v1/series`

**Example Usage:**
```python
get_log_series(
    match=['{namespace="production"}', '{job="api"}'],
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z"
)
```

---

## Epic 3: Metrics & Statistics

### US-3.1: Get Index Statistics
**As an** AI agent
**I want to** view Loki index statistics
**So that** I can understand log volume and storage

**Acceptance Criteria:**
- Return index chunk statistics
- Show streams and entries counts
- Include storage size information
- Show time range coverage

**API Endpoint:** `GET /loki/api/v1/index/stats`

### US-3.2: Query Log Volume Metrics
**As an** AI agent
**I want to** query log volume over time
**So that** I can identify traffic patterns and spikes

**Acceptance Criteria:**
- Return log volume as metric query
- Support aggregation by labels
- Show bytes and entry counts
- Support step parameter for resolution

**Example LogQL:**
```
sum(rate({namespace="production"}[5m])) by (app)
```

---

## Epic 4: Advanced Log Analysis

### US-4.1: Detect Log Patterns
**As an** AI agent
**I want to** automatically detect common log patterns
**So that** I can identify recurring messages

**Acceptance Criteria:**
- Analyze log entries for patterns
- Group similar log lines
- Return pattern templates with occurrence counts
- Support pattern extraction from unstructured logs

### US-4.2: Extract Structured Fields
**As an** AI agent
**I want to** extract JSON fields from logs
**So that** I can analyze structured log data

**Acceptance Criteria:**
- Parse JSON log lines
- Extract specific fields using JSONPath
- Support nested field access
- Handle malformed JSON gracefully

**Example Usage:**
```python
extract_json_fields(
    query='{app="api"} | json',
    field_path="$.error.message",
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T11:00:00Z"
)
```

### US-4.3: Parse Logfmt Logs
**As an** AI agent
**I want to** parse logfmt format logs
**So that** I can analyze structured key-value logs

**Acceptance Criteria:**
- Parse logfmt log lines
- Extract key-value pairs
- Support filtering on extracted fields
- Handle quoted values

**Example LogQL:**
```
{job="api"} | logfmt | level="error"
```

### US-4.4: Analyze Log Frequency
**As an** AI agent
**I want to** analyze log frequency over time
**So that** I can identify traffic patterns and anomalies

**Acceptance Criteria:**
- Count log entries per time bucket
- Support grouping by labels
- Calculate rates and derivatives
- Identify sudden spikes or drops

---

## Epic 5: Error & Incident Investigation

### US-5.1: Find Error Patterns
**As an** AI agent
**I want to** find common error patterns in logs
**So that** I can quickly identify the most frequent issues

**Acceptance Criteria:**
- Search for error-level logs
- Group by error message similarity
- Return top N error patterns
- Include occurrence counts and timestamps
- Support filtering by service/namespace

**Example Usage:**
```python
find_error_patterns(
    namespace="production",
    service="api",
    start="2024-01-15T00:00:00Z",
    end="2024-01-15T23:59:59Z",
    limit=10
)
```

### US-5.2: Get Error Spike Timeline
**As an** AI agent
**I want to** visualize error spike timelines
**So that** I can identify when incidents started

**Acceptance Criteria:**
- Calculate error rate over time
- Identify spike points above baseline
- Return timeline with spike annotations
- Compare to normal error rates

### US-5.3: Extract Stack Traces
**As an** AI agent
**I want to** extract stack traces from error logs
**So that** I can understand error root causes

**Acceptance Criteria:**
- Identify multi-line stack traces
- Parse stack frame information
- Group by exception type
- Link to source code locations

### US-5.4: Find Similar Errors
**As an** AI agent
**I want to** find errors similar to a given error signature
**So that** I can understand error frequency and patterns

**Acceptance Criteria:**
- Match error signatures
- Find similar error messages
- Return occurrence timeline
- Group by affected components

### US-5.5: Get Surrounding Context Logs
**As an** AI agent
**I want to** retrieve logs before and after a specific timestamp
**So that** I can understand the context around an error

**Acceptance Criteria:**
- Accept target timestamp
- Return N logs before and after
- Preserve log ordering
- Include all relevant labels

**Example Usage:**
```python
get_surrounding_logs(
    stream_selector='{namespace="prod",pod="api-123"}',
    timestamp="2024-01-15T10:30:45.123Z",
    before_lines=50,
    after_lines=50
)
```

### US-5.6: Correlate Logs with Traces
**As an** AI agent
**I want to** find logs related to a trace ID
**So that** I can correlate logs with distributed traces

**Acceptance Criteria:**
- Search logs by trace ID
- Support multiple trace ID formats
- Return all logs for a trace
- Sort chronologically across services

**Example Usage:**
```python
trace_request_logs(
    trace_id="abc123def456",
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T11:00:00Z"
)
```

---

## Epic 6: Multi-Pod/Container Analysis

### US-6.1: Find Related Pods Logs
**As an** AI agent
**I want to** retrieve logs from all pods of a deployment
**So that** I can analyze logs across replicas

**Acceptance Criteria:**
- Support pod name pattern matching
- Include all pods in deployment
- Support container filtering
- Aggregate logs from multiple pods

**Example Usage:**
```python
find_related_pods_logs(
    pod_name_pattern="api-*",
    namespace="production",
    container="app",
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T11:00:00Z"
)
```

---

## Epic 7: Performance & Health

### US-7.1: Check Query Performance
**As an** AI agent
**I want to** monitor query performance metrics
**So that** I can optimize slow queries

**Acceptance Criteria:**
- Return query execution time
- Show bytes processed
- Include series/chunk statistics
- Warn on slow queries

### US-7.2: Detect Slow Queries
**As an** AI agent
**I want to** identify slow query patterns
**So that** I can optimize log queries

**Acceptance Criteria:**
- Track query execution times
- Identify queries exceeding thresholds
- Suggest query optimizations
- Show cardinality impact

---

## Epic 8: Status & Health Checks

### US-8.1: Check Loki Health
**As an** AI agent
**I want to** check Loki health status
**So that** I can verify the service is operational

**Acceptance Criteria:**
- Return 200 if healthy
- Quick response for monitoring

**API Endpoint:** `GET /ready`

### US-8.2: Get Ingester Ring Status
**As an** AI agent
**I want to** view the ingester ring status
**So that** I can verify all ingesters are healthy

**Acceptance Criteria:**
- Return all ingester states
- Show ring membership
- Include heartbeat timestamps

**API Endpoint:** `GET /loki/api/v1/status/buildinfo` or similar

---

## Non-Functional Requirements

### NFR-1: Authentication
- Support Bearer token authentication
- Support basic authentication
- Support API key headers
- Read from environment variables (LOKI_URL, LOKI_TOKEN)
- Support custom headers (X-Scope-OrgID for multi-tenancy)

### NFR-2: Read-Only Safety
- Block all write operations
- Only allow GET and read-only POST endpoints
- No log ingestion capabilities
- Clear error messages for blocked operations

### NFR-3: Multi-Tenancy Support
- Support X-Scope-OrgID header
- Allow tenant selection per query
- Default to configured tenant

### NFR-4: Error Handling
- Return structured error responses
- Include HTTP status codes
- Provide helpful error messages
- Handle timeout errors
- Log errors for debugging

### NFR-5: Performance
- Connection pooling for HTTP requests
- Configurable timeouts (default: 30s)
- Stream large result sets
- Efficient JSON parsing
- Context manager for resource cleanup

### NFR-6: Time Handling
- Support RFC3339 timestamps
- Support relative time (now-15m, now-1h)
- Support Unix timestamps (nanoseconds)
- Automatic timezone conversion

---

## Technical Implementation

### Technology Stack
- **Framework:** FastMCP 2.0
- **HTTP Client:** httpx (async support)
- **Python Version:** 3.12+
- **Type Hints:** Full type coverage
- **Documentation:** Comprehensive docstrings

### Project Structure
```
loki-mcp-server/
├── pyproject.toml
├── README.md
├── USER_STORIES.md
├── src/
│   └── loki_mcp_server/
│       ├── __init__.py
│       ├── __main__.py
│       ├── server.py           # FastMCP server setup
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── registry.py     # Tool registration
│       │   ├── query.py        # Query tools
│       │   ├── labels.py       # Label tools
│       │   ├── analysis.py     # Analysis helpers
│       │   └── investigation.py # Incident investigation
│       └── utils/
│           ├── __init__.py
│           ├── client.py       # Loki HTTP client
│           ├── logql.py        # LogQL helpers
│           └── time.py         # Time parsing
└── tests/
    ├── test_client.py
    ├── test_tools.py
    └── test_server.py
```

### Dependencies
```toml
dependencies = [
    "mcp>=1.24.0",
    "fastmcp>=2.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
    "python-dateutil>=2.8.0",
]
```

---

## LogQL Query Examples

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

---

## References
- [Loki HTTP API Documentation](https://grafana.com/docs/loki/latest/reference/loki-http-api/)
- [LogQL Documentation](https://grafana.com/docs/loki/latest/query/)
- [LogQL Examples](https://grafana.com/docs/loki/latest/query/query_examples/)
- [FastMCP Documentation](https://gofastmcp.com/)
