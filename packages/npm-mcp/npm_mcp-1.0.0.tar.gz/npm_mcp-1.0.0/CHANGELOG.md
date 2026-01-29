# Changelog

All notable changes to the NPM MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Stream management tools (2 tools)
- Redirection and dead host management tools (2 tools)
- User management tools (2 tools)
- System and reporting tools (4 tools)
- Bulk operations and cross-instance tools

## [0.2.0] - 2025-10-27 - Phase 2 Complete

### Added - MCP Server & Core Tools

#### Server Infrastructure (Sessions 11-12)
- FastMCP server with async lifespan management for Phase 1 component initialization
- ServerContext class for sharing config, auth, and instance manager across tools
- MCP server entry point (`__main__.py`) with stdio transport support
- Graceful startup and shutdown with proper resource cleanup
- **Test Coverage**: 100% for server core

#### Instance Management Tools (Session 13) - 7 Tools
- `npm_manage_instance`: Create, update, delete, and test NPM instances
- `npm_get_instance`: Get detailed instance information with credential masking
- `npm_list_instances`: List all instances with filtering and status
- `npm_select_instance`: Set active instance for subsequent operations
- `npm_update_instance_credentials`: Securely rotate instance credentials
- `npm_validate_instance_config`: Pre-flight validation for instance configuration
- `npm_set_default_instance`: Change default instance designation
- **Test Coverage**: 89.96% (40 tests passing)

#### Proxy Host Management Tools (Session 14) - 3 Tools
- `npm_manage_proxy_host`: Full CRUD operations for reverse proxy hosts
  - Create with domain routing, SSL, and advanced config
  - Update proxy settings and enable/disable hosts
  - Delete proxy hosts
- `npm_list_proxy_hosts`: List all proxy hosts with filtering by domain and status
- `npm_get_proxy_host`: Get detailed proxy host information by ID or domain
- Support for location-based routing and custom Nginx configuration
- **Test Coverage**: 83.46% (30+ tests passing)

#### Certificate Management Tools (Session 15) - 3 Tools
- `npm_list_certificates`: List SSL/TLS certificates with expiration tracking
  - Filter by expiring soon (configurable threshold)
  - Filter by provider (Let's Encrypt / Custom)
  - Filter by domain name
- `npm_manage_certificate`: Full certificate lifecycle management
  - Let's Encrypt automatic certificates (HTTP challenge)
  - Let's Encrypt wildcard certificates (DNS challenge with provider support)
  - Custom certificate uploads (PEM format)
  - Certificate renewal
  - Certificate deletion
- `npm_validate_certificate`: Pre-flight validation for certificate configuration
- Timezone-aware datetime handling for accurate expiration tracking
- **Test Coverage**: 84.65% (26 tests passing)

#### Access List Management Tools (Session 15) - 2 Tools
- `npm_list_access_lists`: List IP-based access control lists with client counts
- `npm_manage_access_list`: Full CRUD operations for access lists
  - IP-based access control (allow/deny directives)
  - IPv4 and IPv6 support with CIDR notation
  - HTTP Basic Authentication integration
  - Satisfy any (OR) or satisfy all (AND) logic
  - Pass authentication to backend option
- **Test Coverage**: 95.96% (23 tests passing)

### Technical Improvements
- Comprehensive parameter validation before API calls for better error messages
- Structured error handling with actionable error messages
- Context-aware logging for all tool operations
- Multi-instance support across all tools
- Graceful degradation for optional NPM API endpoints
- Early parameter validation to fail fast on invalid input

### Testing
- **Total Tests**: 555 tests (535 passing)
- **Overall Coverage**: 86.44% (exceeds 80% target)
- **Phase 2 Tools Coverage**: 79.58% - 95.96%
- Test-Driven Development (TDD) methodology for all implementations
- Comprehensive mocking strategy with AsyncMock and httpx.MockTransport
- Integration test suite for full-stack workflows

### Documentation
- Updated README.md with Phase 2 completion status and tool examples
- Comprehensive session summaries (Sessions 11-15)
- Tool usage examples for natural language interactions
- Phase 2 completion documentation with metrics

### Bug Fixes
- Fixed timezone-aware datetime comparisons in certificate expiration tracking
- Fixed parameter validation timing to avoid confusing error messages
- Fixed control flow in conditional statements for clarity
- Fixed graceful degradation in validation endpoints

## [0.1.0] - 2025-10-26 - Phase 1 Complete

### Added - Foundation Layer

#### Configuration System (Sessions 1-4)
- YAML-based configuration with environment variable support
- Multi-instance NPM configuration with validation
- Credential encryption using Fernet symmetric encryption
- Environment variable substitution with `${VAR}` syntax
- Secure key generation and storage
- Global settings (timeout, retry, logging)
- **Test Coverage**: 96.05% (48 tests passing)

#### Authentication System (Sessions 5-6)
- JWT token authentication with NPM API
- Automatic token caching (in-memory and disk-based)
- Token expiration detection and automatic refresh
- Proactive token refresh before expiration
- Multi-instance authentication support
- Encrypted disk-based token cache
- Concurrent authentication handling
- **Test Coverage**: 82.93% (49 tests passing)

#### HTTP Client Layer (Sessions 7-8)
- Async HTTP client using httpx
- Configurable retry logic with exponential backoff
- Connection pooling and reuse
- Timeout handling (connect, read, write)
- Automatic error handling for transient failures
- Structured logging for all HTTP operations
- Context manager support for proper cleanup
- **Test Coverage**: 71.52% (31 tests passing)

#### NPM Client (Session 8)
- NPM-specific HTTP client wrapping generic HTTP client
- Automatic JWT token injection in Authorization headers
- Base URL construction from instance configuration
- 401 handling with automatic re-authentication
- All HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Custom header preservation
- **Test Coverage**: 75.74% (16 tests passing)

#### Pydantic Models (Session 9)
- ProxyHost model with full validation
- Certificate model with provider-specific fields
- AccessList model with IP and HTTP auth support
- Stream model for TCP/UDP forwarding
- Redirection and DeadHost models
- User and Settings models
- Comprehensive validation rules and constraints
- **Test Coverage**: 90%+ for all models (46 tests passing)

#### Instance Manager (Session 10)
- Multi-instance NPM management
- NPM client connection pooling and reuse
- Active instance selection and context
- Dynamic instance management (add/remove at runtime)
- Connection testing and validation
- Thread-safe client access
- Proper resource cleanup
- **Test Coverage**: 93.25% (54 tests passing)

#### Logging System (Session 9)
- Structured logging using structlog
- Context-aware log messages
- Configurable log levels
- JSON output for production environments
- Colored output for development
- No sensitive data in logs (credential masking)
- **Test Coverage**: 96.49% (7 tests passing)

### Testing Infrastructure
- Comprehensive pytest setup with async support
- pytest-asyncio for async function testing
- pytest-cov for coverage reporting
- pytest-mock for mocking dependencies
- httpx.MockTransport for HTTP client testing
- Fixture-based test organization
- **Total Phase 1 Tests**: 360 tests passing
- **Overall Phase 1 Coverage**: 88.32%

### Development Tools
- ruff for linting and formatting (PEP 8 compliance)
- mypy for static type checking
- pytest with coverage reporting
- uv for fast dependency management
- Pre-commit hooks for code quality

### Documentation
- Comprehensive PRD (Product Requirements Document) - 67 pages
- Tool Catalog with all 28 planned tools - 50 pages
- Research Summary - 45 pages
- API analysis and endpoint documentation
- Architecture diagrams and decision records
- Session summaries for all development sessions

## [0.0.1] - 2025-10-20 - Project Initialization

### Added
- Initial project structure
- pyproject.toml with dependencies
- pytest configuration
- Git repository setup
- Claude Code project configuration
- Research and planning documentation
- NPM API analysis

### Documentation
- Product Requirements Document (PRD)
- Research findings
- Initial architecture design
- Tool specifications

---

## Version History

- **v0.2.0** (2025-10-27): Phase 2 - MCP Server & 15 Core Tools
- **v0.1.0** (2025-10-26): Phase 1 - Foundation Layer Complete
- **v0.0.1** (2025-10-20): Project Initialization

## Links

- [Product Requirements Document](./docs/PRD.md)
- [Tool Catalog](./docs/TOOL_CATALOG.md)
- [GitHub Repository](https://github.com/wadew/npm-mcp)
