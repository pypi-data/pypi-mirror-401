"""Constants for NPM MCP Server.

This module centralizes all constant values used throughout the application
to prevent string duplication and improve maintainability.
"""

# =============================================================================
# API Endpoints
# =============================================================================

# Nginx resource endpoints
API_PROXY_HOSTS = "/api/nginx/proxy-hosts"
API_CERTIFICATES = "/api/nginx/certificates"
API_ACCESS_LISTS = "/api/nginx/access-lists"
API_STREAMS = "/api/nginx/streams"
API_REDIRECTIONS = "/api/nginx/redirection-hosts"
API_DEAD_HOSTS = "/api/nginx/dead-hosts"

# User management endpoint
API_USERS = "/api/users"

# Authentication endpoint
API_TOKENS = "/api/tokens"

# Settings endpoint
API_SETTINGS = "/api/settings"

# Audit log endpoint
API_AUDIT_LOG = "/api/audit-log"

# Reports endpoint
API_REPORTS = "/api/reports"

# =============================================================================
# Security Constants
# =============================================================================

# Redacted placeholder for sensitive data in logs/output
REDACTED = "***REDACTED***"

# =============================================================================
# Default Values
# =============================================================================

# Default port for NPM API
DEFAULT_NPM_PORT = 81

# Default timeout in seconds
DEFAULT_TIMEOUT = 30

# Default retry attempts
DEFAULT_RETRY_ATTEMPTS = 3

# Default batch size for bulk operations
DEFAULT_BATCH_SIZE = 10

# Default pagination limit
DEFAULT_PAGE_LIMIT = 50

# =============================================================================
# Validation Constants
# =============================================================================

# Port range
MIN_PORT = 1
MAX_PORT = 65535

# Maximum parameters limit (SonarQube S107 threshold)
MAX_FUNCTION_PARAMS = 13
