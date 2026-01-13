# Changelog

All notable changes to the Prometheus MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-10

### Added

#### Core Functionality
- Complete read-only Prometheus MCP server implementation
- FastMCP 2.0 integration with comprehensive tool registry
- Full type hints for Python 3.12+
- Comprehensive error handling and logging

#### Query Tools (Epic 1)
- `query_instant` - Execute PromQL instant queries at specific points in time
- `query_range` - Execute PromQL queries over time ranges with configurable step
- `query_exemplars` - Query exemplars for trace correlation

#### Metadata Discovery Tools (Epic 2)
- `list_metrics` - List all available metrics with optional filtering
- `get_metric_metadata` - Get metric type, help text, and metadata
- `list_labels` - List all label names with optional filtering
- `get_label_values` - Get all values for specific labels
- `find_series` - Find time series matching label selectors

#### Target & Scrape Tools (Epic 4)
- `list_targets` - List all scrape targets and their health status
- `get_targets_metadata` - Get metadata about metrics from targets

#### Alert Tools (Epic 5)
- `list_alerts` - List all active alerts (firing and pending)
- `list_rules` - List all recording and alerting rules

#### Configuration & Status Tools (Epic 6)
- `get_config` - Get Prometheus configuration (YAML)
- `get_flags` - Get runtime command-line flags
- `get_runtime_info` - Get version, uptime, and runtime information
- `get_tsdb_stats` - Get TSDB statistics and cardinality info
- `check_health` - Health check endpoint
- `check_readiness` - Readiness check endpoint

#### Authentication & Security
- Bearer token authentication support
- Basic authentication support
- Environment variable configuration
- SSL certificate verification (configurable)
- Strict read-only safety - all write operations blocked

#### HTTP Client
- `PrometheusClient` with connection pooling via httpx
- Automatic authentication header injection
- Timeout configuration per request
- Context manager support for resource cleanup
- Blocked write operations (PUT, DELETE, PATCH)
- Only allowed read-only endpoints (GET and specific POSTs)

#### Utilities
- Time parsing for multiple formats (RFC3339, Unix timestamp, relative)
- Duration formatting and parsing
- PromQL query validation
- Result formatting helpers

#### Documentation
- Comprehensive README with installation and usage guide
- Detailed USER_STORIES.md with all Epic requirements
- Example configurations for various scenarios
- Docker Compose setup for local testing
- Example Prometheus configuration and alert rules

#### Examples
- Claude Desktop configuration examples (local, remote, auth, k8s)
- Docker Compose setup with Prometheus, Node Exporter, cAdvisor
- Example alert rules and recording rules
- Testing guide and troubleshooting documentation

#### Development
- Project structure following best practices
- Comprehensive docstrings for all functions
- Type hints throughout the codebase
- `.env.example` for environment configuration
- `.gitignore` for Python projects
- MIT License

### Implementation Status

#### ✅ Completed (Epics 1-6)
- Epic 1: Core Metrics Querying - **Complete**
- Epic 2: Metadata Discovery - **Complete**
- Epic 3: Series Discovery - **Complete** (included in Epic 2)
- Epic 4: Target & Scrape Discovery - **Complete**
- Epic 5: Alerting - **Complete**
- Epic 6: Configuration & Status - **Complete**

#### 🚧 Future Enhancements (Epics 7-9)
- Epic 7: Advanced Analysis - **Not Implemented**
  - Spike detection
  - Time range comparison
  - Top resource consumers
  - Correlation analysis
- Epic 8: Federation & Remote Read - **Not Implemented**
  - Federation endpoint support
- Epic 9: Safety & Performance - **Partially Implemented**
  - Request timeout handling - ✅ Complete
  - Result size limiting - 🚧 Planned
  - Query cost estimation - 🚧 Planned

#### Non-Functional Requirements
- NFR-1: Authentication - ✅ Complete
- NFR-2: Read-Only Safety - ✅ Complete
- NFR-3: Error Handling - ✅ Complete
- NFR-4: Performance - ✅ Complete
- NFR-5: Observability - 🚧 Partial (basic logging)

### Technical Details

**Dependencies:**
- mcp >= 1.24.0
- fastmcp >= 2.0.0
- httpx >= 0.27.0
- pydantic >= 2.0.0
- python-dateutil >= 2.8.0

**Python Version:** 3.12+

**Transport Support:**
- stdio (default, for Claude Desktop)
- HTTP
- SSE (Server-Sent Events)

### Breaking Changes
None - Initial release

### Known Limitations
- Advanced analysis tools (Epic 7) not implemented yet
- Federation endpoint (Epic 8) not implemented yet
- Query cost estimation (Epic 9) not implemented yet
- No async support (uses httpx but synchronous calls)

### Migration Guide
N/A - Initial release

## [Unreleased]

### Planned Features
- Epic 7: Advanced analysis helpers (spike detection, correlation)
- Epic 8: Federation endpoint support
- Epic 9: Query cost estimation and result size limiting
- Async query support for better performance
- Query result caching
- Prometheus remote write inspection (read-only)
- Multi-Prometheus support (query multiple instances)
- Advanced logging and telemetry
- Integration tests with real Prometheus
- Performance benchmarks

---

## Version History

- **0.1.0** (2024-01-10) - Initial release with core functionality (Epics 1-6)
