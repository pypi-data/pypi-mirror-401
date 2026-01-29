# MCP Tool Catalog - Nginx Proxy Manager

This document provides a comprehensive catalog of all MCP tools available in the Nginx Proxy Manager MCP server.

**Total Tools**: 28 semantic tools grouped into 9 categories (100% PRD specification)

**Phase 4 Complete**: Includes unified `npm_bulk_operations` tool with 5 operations

---

## Table of Contents

1. [Instance Management](#1-instance-management-7-tools)
2. [Proxy Host Management](#2-proxy-host-management-3-tools)
3. [Certificate Management](#3-certificate-management-3-tools)
4. [Access Control](#4-access-control-2-tools)
5. [Stream Management](#5-stream-management-2-tools)
6. [Redirection & Dead Hosts](#6-redirection--dead-hosts-2-tools)
7. [User Management](#7-user-management-2-tools)
8. [System & Reporting](#8-system--reporting-4-tools)
9. [Bulk Operations](#9-bulk-operations-3-tools)

---

## 1. Instance Management (7 tools)

**Enhanced with Full CRUD**: Instance management now supports complete CRUD operations with persistent configuration storage, enabling LLMs to dynamically manage NPM instances without manual file editing.

### 1.1 `npm_manage_instance`

**Purpose**: Full CRUD operations on NPM instance configurations (create, update, delete, test)

**Parameters**:
```json
{
  "operation": "create|update|delete|test", // Required: Operation type
  "instance_name": "production",            // Required: Unique identifier

  // Connection details (required for create/update):
  "host": "npm.example.com",               // Hostname or IP address
  "port": 81,                              // Port number (1-65535), default: 81
  "use_https": true,                       // Use HTTPS for API, default: false
  "verify_ssl": true,                      // Verify SSL certificates, default: true

  // Authentication (either username/password OR api_token):
  "username": "admin@example.com",         // Username for authentication
  "password": "secretpassword",            // Password for authentication
  "api_token": "eyJhbGc...",               // Alternative: pre-generated API token

  // Configuration options:
  "set_as_default": true,                  // Set as default instance, default: false
  "persist_to_file": true,                 // Save to YAML config file, default: false
  "config_file": "~/.npm-mcp/instances.yaml", // Config file path
  "description": "Production NPM server",  // Instance description
  "tags": ["production", "public"],        // Tags for organization
  "test_connection": true,                 // Test connection before adding
  "timeout": 30                            // Connection timeout in seconds
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "instance": {
    "name": "production",
    "host": "npm.example.com",
    "port": 81,
    "use_https": true,
    "is_default": true,
    "connection_tested": true,
    "connection_status": "connected",
    "persisted_to_file": true,
    "config_file": "/Users/user/.npm-mcp/instances.yaml",
    "description": "Production NPM server",
    "tags": ["production", "public"]
  }
}
```

**Example Usage**:
> "Add NPM instance 'homelab' at 192.168.1.100 with username admin@local and password homelab123, and save it to my config file"

> "Update the production instance to use HTTPS"

> "Delete the testing instance"

---

### 1.2 `npm_get_instance`

**Purpose**: Get detailed configuration for a specific instance

**Parameters**:
```json
{
  "instance_name": "production",           // Required: Instance name
  "show_credentials": false                // Optional: Show masked credentials, default: false
}
```

**Returns**:
```json
{
  "name": "production",
  "host": "npm.example.com",
  "port": 81,
  "use_https": true,
  "verify_ssl": true,
  "has_username": true,
  "username": "admin@example.com",
  "has_password": true,
  "password": "***MASKED***",
  "has_token": false,
  "is_default": true,
  "is_connected": true,
  "last_connection_test": "2025-10-26T12:00:00Z",
  "connection_status": "connected",
  "token_cached": true,
  "token_expires_at": "2035-10-26T12:00:00Z",
  "description": "Production NPM server",
  "tags": ["production", "public"],
  "persisted_to_file": true
}
```

**Example Usage**:
> "Show me the configuration for the production instance"

> "Get details about the homelab NPM server"

---

### 1.3 `npm_list_instances`

**Purpose**: List all configured NPM instances with filtering

**Parameters**:
```json
{
  "filter_tags": ["production"],          // Optional: Filter by tags
  "filter_connected": true,               // Optional: Only show connected instances
  "show_credentials": false,              // Optional: Show masked credentials, default: false
  "include_test_results": false           // Optional: Include last connection test details
}
```

**Returns**:
```json
{
  "instances": [
    {
      "name": "production",
      "host": "npm.example.com",
      "port": 81,
      "use_https": true,
      "is_default": true,
      "is_connected": true,
      "last_tested": "2025-10-26T10:30:00Z",
      "tags": ["production", "public"],
      "persisted_to_file": true
    },
    {
      "name": "homelab",
      "host": "192.168.1.100",
      "port": 81,
      "use_https": false,
      "is_default": false,
      "is_connected": true,
      "last_tested": "2025-10-26T10:29:00Z",
      "tags": ["homelab", "local"],
      "persisted_to_file": true
    }
  ],
  "total": 2,
  "connected": 2
}
```

**Example Usage**:
> "Show me all configured NPM instances"

> "List only connected instances with production tag"

---

### 1.4 `npm_select_instance`

**Purpose**: Set the active instance for subsequent operations

**Parameters**:
```json
{
  "instance_name": "staging",             // Required: Instance to select
  "test_connection": true                 // Optional: Test connection before selecting, default: true
}
```

**Returns**:
```json
{
  "success": true,
  "selected_instance": "staging",
  "host": "npm-staging.example.com",
  "connection_status": "connected",
  "message": "All subsequent operations will use the 'staging' instance"
}
```

**Example Usage**:
> "Switch to the staging instance"

> "Select the homelab NPM server"

---

### 1.5 `npm_update_instance_credentials`

**Purpose**: Rotate credentials for an instance without recreating it

**Parameters**:
```json
{
  "instance_name": "production",          // Required: Instance name

  // New credentials (provide username/password OR api_token):
  "new_username": "admin@example.com",    // New username
  "new_password": "newsecretpassword",    // New password
  "new_api_token": "eyJhbGc...",          // Alternative: new API token

  // Options:
  "test_before_applying": true,           // Test new credentials first, default: true
  "persist_to_file": true,                // Update config file, default: false
  "invalidate_cached_tokens": true        // Clear old JWT tokens, default: true
}
```

**Returns**:
```json
{
  "success": true,
  "instance_name": "production",
  "credentials_updated": true,
  "test_successful": true,
  "persisted_to_file": true,
  "tokens_invalidated": true,
  "message": "Credentials updated and tested successfully"
}
```

**Example Usage**:
> "Update the production instance password to 'newpass456' and save it"

> "Rotate the API token for the homelab instance"

---

### 1.6 `npm_validate_instance_config`

**Purpose**: Validate instance configuration before adding (pre-flight check)

**Parameters**: Same as `npm_manage_instance` create operation

**Returns**:
```json
{
  "valid": true,
  "validation_results": [
    {
      "check": "host_reachable",
      "status": "passed",
      "message": "Host npm.example.com is reachable",
      "duration_ms": 45
    },
    {
      "check": "port_accessible",
      "status": "passed",
      "message": "Port 81 is accessible",
      "duration_ms": 12
    },
    {
      "check": "ssl_certificate",
      "status": "passed",
      "message": "SSL certificate is valid",
      "duration_ms": 78
    },
    {
      "check": "authentication",
      "status": "passed",
      "message": "Credentials are valid",
      "duration_ms": 342
    },
    {
      "check": "api_version",
      "status": "passed",
      "message": "NPM API version 2.11.3 detected",
      "duration_ms": 15
    },
    {
      "check": "network_latency",
      "status": "passed",
      "message": "Average latency: 142ms",
      "duration_ms": 142
    }
  ],
  "warnings": [
    "Response time is higher than recommended (>100ms)"
  ],
  "errors": [],
  "total_validation_time_ms": 634
}
```

**Example Usage**:
> "Validate this NPM configuration before I add it: host npm.test.com, username admin@test, password test123"

> "Check if I can connect to 192.168.1.50 on port 81"

---

### 1.7 `npm_set_default_instance`

**Purpose**: Change which instance is the default

**Parameters**:
```json
{
  "instance_name": "homelab",             // Required: Instance to set as default
  "persist_to_file": true                 // Optional: Update config file, default: false
}
```

**Returns**:
```json
{
  "success": true,
  "previous_default": "production",
  "new_default": "homelab",
  "persisted_to_file": true,
  "message": "Default instance changed from 'production' to 'homelab'"
}
```

**Example Usage**:
> "Make the homelab instance the default"

> "Set production as the default NPM server and save it"

---

## 2. Proxy Host Management (3 tools)

### 2.1 `npm_manage_proxy_host`

**Purpose**: Create, update, delete, enable, or disable proxy hosts

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete|enable|disable
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete/enable/disable:
  "host_id": 42,                           // Proxy host ID

  // Required for create/update:
  "domain_names": ["api.example.com", "www.api.example.com"],
  "forward_host": "192.168.1.100",
  "forward_port": 3000,
  "forward_scheme": "http",                // http|https

  // Optional SSL configuration:
  "certificate_id": 5,                     // Use existing certificate
  "force_ssl": true,                       // Redirect HTTP to HTTPS
  "hsts_enabled": true,                    // Enable HSTS
  "hsts_subdomains": false,                // Include subdomains in HSTS

  // Optional features:
  "http2_support": true,
  "websocket_support": true,
  "block_exploits": true,
  "caching_enabled": false,

  // Optional access control:
  "access_list_id": 3,                     // Apply access list

  // Optional advanced configuration:
  "advanced_config": "proxy_read_timeout 300s;",

  // Optional location-based routing:
  "locations": [
    {
      "path": "/api",
      "forward_scheme": "http",
      "forward_host": "192.168.1.101",
      "forward_port": 8080,
      "forward_path": "/v1/api",
      "advanced_config": ""
    }
  ]
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "proxy_host": {
    "id": 42,
    "domain_names": ["api.example.com", "www.api.example.com"],
    "forward_host": "192.168.1.100",
    "forward_port": 3000,
    "forward_scheme": "http",
    "enabled": true,
    "ssl_forced": true,
    "certificate_id": 5,
    "created_on": "2025-10-26T10:30:00Z",
    "modified_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create a proxy host for api.example.com pointing to 192.168.1.100:3000 with SSL certificate ID 5 and force HTTPS"

> "Update proxy host ID 42 to enable caching and HTTP/2 support"

> "Disable proxy host ID 42"

---

### 2.2 `npm_list_proxy_hosts`

**Purpose**: List all proxy hosts with optional filtering

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "domain_filter": "example.com",          // Optional: Filter by domain
  "enabled_only": true,                    // Optional: Show only enabled hosts
  "page": 1,                               // Optional: Page number
  "limit": 50                              // Optional: Results per page
}
```

**Returns**:
```json
{
  "proxy_hosts": [
    {
      "id": 42,
      "domain_names": ["api.example.com", "www.api.example.com"],
      "forward_host": "192.168.1.100",
      "forward_port": 3000,
      "enabled": true,
      "ssl_forced": true,
      "certificate_id": 5
    }
  ],
  "total": 15,
  "page": 1,
  "pages": 1
}
```

**Example Usage**:
> "List all proxy hosts"

> "Show me all enabled proxy hosts for example.com domain"

---

### 2.3 `npm_get_proxy_host`

**Purpose**: Get detailed information about a specific proxy host

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "host_id": 42,                           // Required: Proxy host ID (or domain_name)
  "domain_name": "api.example.com"         // Alternative: Search by domain
}
```

**Returns**:
```json
{
  "id": 42,
  "domain_names": ["api.example.com", "www.api.example.com"],
  "forward_host": "192.168.1.100",
  "forward_port": 3000,
  "forward_scheme": "http",
  "enabled": true,
  "ssl_forced": true,
  "hsts_enabled": true,
  "http2_support": true,
  "block_exploits": true,
  "caching_enabled": false,
  "allow_websocket_upgrade": true,
  "certificate": {
    "id": 5,
    "nice_name": "Example API Certificate",
    "domain_names": ["*.example.com"],
    "expires_on": "2026-10-26T00:00:00Z"
  },
  "access_list": {
    "id": 3,
    "name": "Office Network"
  },
  "locations": [
    {
      "path": "/api",
      "forward_scheme": "http",
      "forward_host": "192.168.1.101",
      "forward_port": 8080
    }
  ],
  "created_on": "2025-10-26T10:30:00Z",
  "modified_on": "2025-10-26T10:30:00Z",
  "owner": {
    "id": 1,
    "name": "Admin User",
    "email": "admin@example.com"
  }
}
```

**Example Usage**:
> "Show me details for proxy host ID 42"

> "Get information about the proxy host for api.example.com"

---

## 3. Certificate Management (3 tools)

### 3.1 `npm_manage_certificate`

**Purpose**: Create, update, delete, or renew SSL certificates

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete|renew
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete/renew:
  "cert_id": 5,                            // Certificate ID

  // Required for create:
  "provider": "letsencrypt",               // letsencrypt|custom
  "nice_name": "Example Wildcard Cert",
  "domain_names": ["*.example.com", "example.com"],

  // Let's Encrypt options:
  "letsencrypt_email": "admin@example.com",
  "letsencrypt_agree_tos": true,
  "dns_challenge": true,                   // Use DNS challenge (for wildcards)
  "dns_provider": "cloudflare",            // cloudflare|route53|digitalocean|etc
  "dns_credentials": "{\"api_token\":\"...\"}",  // Provider-specific credentials
  "propagation_seconds": 60,               // DNS propagation wait time

  // Custom certificate options:
  "custom_certificate": "-----BEGIN CERTIFICATE-----\n...",
  "custom_certificate_key": "-----BEGIN PRIVATE KEY-----\n..."
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "certificate": {
    "id": 5,
    "provider": "letsencrypt",
    "nice_name": "Example Wildcard Cert",
    "domain_names": ["*.example.com", "example.com"],
    "expires_on": "2026-10-26T00:00:00Z",
    "days_until_expiry": 365,
    "created_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create a Let's Encrypt certificate for *.example.com and example.com using Cloudflare DNS challenge with email admin@example.com"

> "Renew certificate ID 5"

> "Delete certificate ID 7"

---

### 3.2 `npm_list_certificates`

**Purpose**: List all certificates with expiration tracking

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "expiring_soon": true,                   // Optional: Certs expiring in < 30 days
  "provider": "letsencrypt",               // Optional: Filter by provider
  "domain_filter": "example.com"           // Optional: Filter by domain
}
```

**Returns**:
```json
{
  "certificates": [
    {
      "id": 5,
      "provider": "letsencrypt",
      "nice_name": "Example Wildcard Cert",
      "domain_names": ["*.example.com", "example.com"],
      "expires_on": "2026-10-26T00:00:00Z",
      "days_until_expiry": 365,
      "status": "valid"
    },
    {
      "id": 6,
      "provider": "letsencrypt",
      "nice_name": "Old Certificate",
      "domain_names": ["old.example.com"],
      "expires_on": "2025-11-10T00:00:00Z",
      "days_until_expiry": 15,
      "status": "expiring_soon"
    }
  ],
  "total": 10,
  "expiring_soon_count": 2
}
```

**Example Usage**:
> "List all certificates"

> "Show me certificates expiring in the next 30 days"

---

### 3.3 `npm_validate_certificate`

**Purpose**: Validate certificate configuration before creation

**Parameters**: Same as `npm_manage_certificate` with `operation: "create"`

**Returns**:
```json
{
  "valid": true,
  "validation_results": [
    {
      "check": "domain_syntax",
      "status": "passed",
      "message": "All domain names are syntactically valid"
    },
    {
      "check": "dns_records",
      "status": "passed",
      "message": "DNS A records found for all domains"
    },
    {
      "check": "http_reachable",
      "status": "passed",
      "message": "All domains are reachable via HTTP"
    },
    {
      "check": "dns_provider_credentials",
      "status": "passed",
      "message": "DNS provider credentials are valid"
    }
  ],
  "warnings": [
    "Wildcard certificates require DNS challenge"
  ],
  "errors": []
}
```

**Example Usage**:
> "Validate a Let's Encrypt certificate configuration for *.example.com using Cloudflare DNS"

---

## 4. Access Control (2 tools)

### 4.1 `npm_manage_access_list`

**Purpose**: Create, update, or delete access lists

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete:
  "list_id": 3,                            // Access list ID

  // Required for create/update:
  "name": "Office Network",
  "directive": "allow",                    // allow|deny
  "addresses": [
    "192.168.1.0/24",                      // CIDR notation
    "10.0.0.0/8",
    "2001:db8::/32",                       // IPv6 support
    "203.0.113.5"                          // Single IP
  ],
  "satisfy_any": true,                     // true: match any rule | false: match all rules
  "pass_auth": false,                      // Pass authentication to backend

  // Optional HTTP Basic Auth:
  "clients": [
    {
      "username": "john",
      "password": "secretpass123"
    },
    {
      "username": "jane",
      "password": "anotherpass456"
    }
  ]
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "access_list": {
    "id": 3,
    "name": "Office Network",
    "directive": "allow",
    "addresses": ["192.168.1.0/24", "10.0.0.0/8"],
    "satisfy_any": true,
    "pass_auth": false,
    "clients": [
      {"username": "john"},
      {"username": "jane"}
    ],
    "created_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create an access list named 'Office Network' that allows 192.168.1.0/24 and 10.0.0.0/8"

> "Update access list ID 3 to add HTTP basic auth for user john with password secretpass123"

---

### 4.2 `npm_list_access_lists`

**Purpose**: List all access lists

**Parameters**:
```json
{
  "instance_name": "production"            // Optional: Target instance
}
```

**Returns**:
```json
{
  "access_lists": [
    {
      "id": 3,
      "name": "Office Network",
      "directive": "allow",
      "addresses": ["192.168.1.0/24", "10.0.0.0/8"],
      "client_count": 2,
      "created_on": "2025-10-26T10:30:00Z"
    },
    {
      "id": 4,
      "name": "Blocked Countries",
      "directive": "deny",
      "addresses": ["all"],
      "client_count": 0,
      "created_on": "2025-10-25T09:00:00Z"
    }
  ],
  "total": 2
}
```

**Example Usage**:
> "List all access lists"

---

## 5. Stream Management (2 tools)

### 5.1 `npm_manage_stream`

**Purpose**: Create, update, delete, enable, or disable TCP/UDP streams

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete|enable|disable
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete/enable/disable:
  "stream_id": 10,                         // Stream ID

  // Required for create/update:
  "incoming_port": 3306,                   // Port to listen on (1-65535)
  "forwarding_host": "192.168.1.50",       // Target host (IP or hostname)
  "forwarding_port": 3306,                 // Target port
  "tcp_forwarding": true,                  // Enable TCP forwarding
  "udp_forwarding": false,                 // Enable UDP forwarding

  // Optional SSL:
  "certificate_id": 5,                     // Use certificate for SSL termination

  // Metadata:
  "meta": {
    "description": "MySQL Database Stream"
  }
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "stream": {
    "id": 10,
    "incoming_port": 3306,
    "forwarding_host": "192.168.1.50",
    "forwarding_port": 3306,
    "tcp_forwarding": true,
    "udp_forwarding": false,
    "enabled": true,
    "certificate_id": null,
    "created_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create a TCP stream on port 3306 forwarding to 192.168.1.50:3306"

> "Update stream ID 10 to also enable UDP forwarding"

> "Disable stream ID 10"

---

### 5.2 `npm_list_streams`

**Purpose**: List all streams

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "enabled_only": true,                    // Optional: Show only enabled streams
  "protocol": "tcp"                        // Optional: Filter by tcp|udp
}
```

**Returns**:
```json
{
  "streams": [
    {
      "id": 10,
      "incoming_port": 3306,
      "forwarding_host": "192.168.1.50",
      "forwarding_port": 3306,
      "tcp_forwarding": true,
      "udp_forwarding": false,
      "enabled": true
    },
    {
      "id": 11,
      "incoming_port": 5432,
      "forwarding_host": "192.168.1.51",
      "forwarding_port": 5432,
      "tcp_forwarding": true,
      "udp_forwarding": false,
      "enabled": true
    }
  ],
  "total": 5,
  "enabled_count": 2
}
```

**Example Usage**:
> "List all enabled streams"

---

## 6. Redirection & Dead Hosts (2 tools)

### 6.1 `npm_manage_redirection`

**Purpose**: Create, update, or delete URL redirections

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete:
  "redirect_id": 8,                        // Redirection ID

  // Required for create/update:
  "domain_names": ["old.example.com"],
  "forward_scheme": "https",               // http|https|$scheme (preserve)
  "forward_domain_name": "new.example.com",
  "forward_http_code": 301,                // 301|302|307|308
  "preserve_path": true,                   // Append original path to redirect

  // Optional SSL:
  "certificate_id": 5,

  // Optional advanced:
  "advanced_config": ""
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "redirection": {
    "id": 8,
    "domain_names": ["old.example.com"],
    "forward_scheme": "https",
    "forward_domain_name": "new.example.com",
    "forward_http_code": 301,
    "preserve_path": true,
    "created_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create a 301 redirect from old.example.com to https://new.example.com preserving the path"

---

### 6.2 `npm_manage_dead_host`

**Purpose**: Create, update, or delete 404/dead hosts

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete:
  "host_id": 12,                           // Dead host ID

  // Required for create/update:
  "domain_names": ["*.unused.example.com"],

  // Optional SSL:
  "certificate_id": 5
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "dead_host": {
    "id": 12,
    "domain_names": ["*.unused.example.com"],
    "certificate_id": 5,
    "created_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create a dead host for *.unused.example.com to catch all unused subdomains"

---

## 7. User Management (2 tools)

### 7.1 `npm_manage_user`

**Purpose**: Create, update, delete users, or change passwords

**Parameters**:
```json
{
  "operation": "create",                   // Required: create|update|delete|change_password
  "instance_name": "production",           // Optional: Target instance

  // Required for update/delete/change_password:
  "user_id": 5,                            // User ID

  // Required for create:
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",

  // Required for change_password:
  "current_password": "oldpassword",
  "new_password": "newpassword123",

  // Optional for create/update:
  "is_admin": false,
  "permissions": {
    "visibility": "user",                  // all|user
    "proxy_hosts": "manage",               // view|manage
    "redirection_hosts": "manage",
    "dead_hosts": "manage",
    "streams": "manage",
    "access_lists": "manage",
    "certificates": "manage"
  }
}
```

**Returns**:
```json
{
  "success": true,
  "operation": "create",
  "user": {
    "id": 5,
    "name": "John Doe",
    "email": "john@example.com",
    "is_admin": false,
    "permissions": {
      "visibility": "user",
      "proxy_hosts": "manage"
    },
    "created_on": "2025-10-26T10:30:00Z"
  }
}
```

**Example Usage**:
> "Create a user named John Doe with email john@example.com and password securepassword123 with manage permissions for proxy hosts"

> "Change password for user ID 5"

---

### 7.2 `npm_list_users`

**Purpose**: List all users

**Parameters**:
```json
{
  "instance_name": "production"            // Optional: Target instance
}
```

**Returns**:
```json
{
  "users": [
    {
      "id": 1,
      "name": "Admin User",
      "email": "admin@example.com",
      "is_admin": true,
      "created_on": "2025-01-01T00:00:00Z"
    },
    {
      "id": 5,
      "name": "John Doe",
      "email": "john@example.com",
      "is_admin": false,
      "created_on": "2025-10-26T10:30:00Z"
    }
  ],
  "total": 2
}
```

**Example Usage**:
> "List all users"

---

## 8. System & Reporting (4 tools)

### 8.1 `npm_get_system_settings`

**Purpose**: Get current system settings

**Parameters**:
```json
{
  "instance_name": "production"            // Optional: Target instance
}
```

**Returns**:
```json
{
  "default-site": "congratulations",
  "database-version": "20231010",
  "software-version": "2.11.3",
  "letsencrypt-email": "admin@example.com"
}
```

**Example Usage**:
> "Show system settings"

---

### 8.2 `npm_update_system_settings`

**Purpose**: Update system settings

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "settings": {
    "default-site": "congratulations",
    "letsencrypt-email": "newemail@example.com"
  }
}
```

**Returns**:
```json
{
  "success": true,
  "updated_settings": {
    "default-site": "congratulations",
    "letsencrypt-email": "newemail@example.com"
  }
}
```

**Example Usage**:
> "Update Let's Encrypt email to newemail@example.com"

---

### 8.3 `npm_get_audit_logs`

**Purpose**: Retrieve audit logs

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "start_date": "2025-10-01T00:00:00Z",    // Optional: Filter start date
  "end_date": "2025-10-26T23:59:59Z",      // Optional: Filter end date
  "user_id": 1,                            // Optional: Filter by user
  "action_filter": "proxy",                // Optional: Filter by action keyword
  "page": 1,                               // Optional: Page number
  "limit": 100                             // Optional: Results per page
}
```

**Returns**:
```json
{
  "audit_logs": [
    {
      "id": 1523,
      "created_on": "2025-10-26T10:30:00Z",
      "user_id": 1,
      "user_email": "admin@example.com",
      "action": "created",
      "object_type": "proxy-host",
      "object_id": 42,
      "meta": {
        "domain_names": ["api.example.com"]
      }
    }
  ],
  "total": 1523,
  "page": 1,
  "pages": 16
}
```

**Example Usage**:
> "Show audit logs for the last 7 days"

> "Get all audit logs for user ID 1 related to proxy hosts"

---

### 8.4 `npm_get_host_reports`

**Purpose**: Get performance reports for hosts

**Parameters**:
```json
{
  "instance_name": "production",           // Optional: Target instance
  "time_range": "24h",                     // 1h|24h|7d|30d
  "host_ids": [42, 43],                    // Optional: Specific hosts
  "metrics": ["requests", "bandwidth"]     // Optional: Specific metrics
}
```

**Returns**:
```json
{
  "report_period": "24h",
  "generated_at": "2025-10-26T10:30:00Z",
  "hosts": [
    {
      "host_id": 42,
      "domain_names": ["api.example.com"],
      "metrics": {
        "total_requests": 158342,
        "unique_visitors": 2351,
        "bandwidth_mb": 1532.5,
        "avg_response_time_ms": 142,
        "error_rate": 0.02
      }
    }
  ]
}
```

**Example Usage**:
> "Get performance reports for all hosts in the last 24 hours"

---

## 9. Bulk Operations (1 unified tool)

**Note**: All bulk operations are handled by a single unified tool `npm_bulk_operations` with an operation parameter. This design follows MCP best practices for semantic grouping and reduces LLM context overhead.

### 9.1 `npm_bulk_operations`

**Purpose**: Unified tool for performing batch operations across multiple NPM resources efficiently

**Key Features**:
- **5 Operations**: Certificate renewal, host toggling, resource deletion, configuration export/import
- **Concurrent Processing**: Process up to 50 items simultaneously with configurable batch_size
- **Error Resilience**: Continue processing on errors with detailed per-item results
- **Dry-Run Mode**: Preview changes without executing for all operations
- **Advanced Filtering**: Select resources using domain patterns, expiration windows, enabled status
- **Multiple Formats**: Export/import supports JSON and YAML

---

#### Operation 1: `renew_certificates`

**Purpose**: Renew multiple Let's Encrypt certificates concurrently

**Parameters**:
```json
{
  "operation": "renew_certificates",
  "instance_name": "production",           // Optional: Target instance

  // Resource Selection (choose one):
  "resource_ids": [5, 6, 7],              // Specific certificate IDs
  "filters": {
    "expiring_within_days": 30            // Auto-select expiring certs
  },

  // Processing Options:
  "batch_size": 10,                       // Concurrent renewals (1-50)
  "dry_run": false,                       // Preview without executing
  "continue_on_error": true               // Continue if some fail
}
```

**Returns**:
```json
{
  "operation": "renew_certificates",
  "status": "completed",
  "total_items": 15,
  "successful": 13,
  "failed": 2,
  "dry_run": false,
  "results": [
    {
      "resource_id": 5,
      "resource_type": "certificate",
      "action": "renew",
      "status": "success",
      "details": {
        "domain_names": ["example.com"],
        "expires_on": "2026-01-15T00:00:00Z"
      }
    },
    {
      "resource_id": 6,
      "resource_type": "certificate",
      "action": "renew",
      "status": "error",
      "error": "DNS validation failed for *.example.com"
    }
  ],
  "duration_seconds": 45.3,
  "instance_name": "production"
}
```

**Example Usage**:
> "Renew all certificates expiring in the next 30 days"

> "Do a dry run to see which certificates would be renewed"

> "Renew certificates 5, 6, and 7 concurrently"

---

#### Operation 2: `toggle_hosts`

**Purpose**: Enable or disable multiple proxy hosts in bulk

**Parameters**:
```json
{
  "operation": "toggle_hosts",
  "instance_name": "production",
  "action": "disable",                     // enable|disable

  // Resource Selection (choose one):
  "resource_ids": [42, 43, 44],           // Specific host IDs
  "filters": {
    "domain_pattern": "staging",          // Substring match
    "enabled_only": true                  // Only enabled hosts
  },

  // Processing Options:
  "batch_size": 20,
  "dry_run": false,
  "continue_on_error": true
}
```

**Returns**:
```json
{
  "operation": "toggle_hosts",
  "status": "completed",
  "total_items": 25,
  "successful": 25,
  "failed": 0,
  "results": [
    {
      "resource_id": 42,
      "resource_type": "proxy_host",
      "action": "disable",
      "status": "success",
      "details": {
        "domain_names": ["api.staging.example.com"],
        "previous_state": "enabled",
        "new_state": "disabled"
      }
    }
  ],
  "duration_seconds": 8.2
}
```

**Example Usage**:
> "Disable all staging hosts"

> "Enable all hosts matching pattern 'api'"

> "Disable proxy hosts 42, 43, and 44"

---

#### Operation 3: `delete_resources`

**Purpose**: Bulk delete resources with validation

**Parameters**:
```json
{
  "operation": "delete_resources",
  "instance_name": "production",
  "resource_type": "proxy_hosts",          // proxy_hosts|certificates|access_lists|streams|redirections|dead_hosts|users

  // Resource Selection:
  "resource_ids": [100, 101, 102],

  // Processing Options:
  "batch_size": 10,
  "dry_run": true,                        // RECOMMENDED for delete
  "continue_on_error": true
}
```

**Returns**:
```json
{
  "operation": "delete_resources",
  "status": "completed",
  "total_items": 3,
  "successful": 2,
  "failed": 1,
  "dry_run": true,
  "results": [
    {
      "resource_id": 100,
      "resource_type": "proxy_host",
      "action": "delete",
      "status": "success",
      "details": {
        "domain_names": ["old.example.com"]
      }
    },
    {
      "resource_id": 101,
      "resource_type": "proxy_host",
      "action": "delete",
      "status": "error",
      "error": "Resource not found"
    }
  ],
  "duration_seconds": 2.1
}
```

**Example Usage**:
> "Delete old proxy hosts 100, 101, and 102 (do a dry run first)"

> "Delete certificates 5, 6, 7"

> "Delete all unused access lists"

---

#### Operation 4: `export_config`

**Purpose**: Export NPM configuration for backup or migration

**Parameters**:
```json
{
  "operation": "export_config",
  "instance_name": "production",

  // Resource Selection:
  "resource_type": "all",                  // all|proxy_hosts|certificates|access_lists|streams|redirections|dead_hosts|users
  "resource_ids": null,                    // Optional: specific IDs only

  // Export Options:
  "export_format": "json",                 // json|yaml

  // Processing Options:
  "dry_run": false,
  "continue_on_error": true
}
```

**Returns**:
```json
{
  "operation": "export_config",
  "status": "completed",
  "total_items": 127,
  "successful": 127,
  "failed": 0,
  "results": [
    {
      "resource_type": "export_metadata",
      "status": "success",
      "details": {
        "version": "1.0",
        "exported_at": "2025-10-28T12:00:00Z",
        "instance_name": "production",
        "format": "json"
      }
    },
    {
      "resource_type": "proxy_hosts",
      "status": "success",
      "details": {
        "count": 45,
        "data": [...]
      }
    },
    {
      "resource_type": "certificates",
      "status": "success",
      "details": {
        "count": 12,
        "data": [...]
      }
    }
  ],
  "duration_seconds": 3.8
}
```

**Export Format** (JSON example):
```json
{
  "version": "1.0",
  "exported_at": "2025-10-28T12:00:00Z",
  "instance_name": "production",
  "resources": {
    "proxy_hosts": [...],
    "certificates": [...],
    "access_lists": [...],
    "streams": [...],
    "redirections": [...],
    "dead_hosts": [...],
    "users": [...]
  }
}
```

**Example Usage**:
> "Export all resources to JSON for backup"

> "Export only proxy hosts and certificates to YAML"

> "Export configuration for migration to new instance"

---

#### Operation 5: `import_config`

**Purpose**: Import configuration from backup or migrate from another instance

**Parameters**:
```json
{
  "operation": "import_config",
  "instance_name": "staging",

  // Import Data (choose format):
  "import_data": {/* config object */},   // Dict format
  "import_data": "{...}",                 // JSON string
  "import_data": "version: 1.0\n...",     // YAML string

  // Import Strategy:
  "import_strategy": "merge",             // merge|replace

  // Processing Options:
  "batch_size": 10,
  "dry_run": true,                        // RECOMMENDED before actual import
  "continue_on_error": true
}
```

**Import Strategies**:
- **merge** (default): Add new resources, update existing ones. Safe, non-destructive.
- **replace**: Delete all existing resources, then import. Use for full restore or instance cloning.

**Returns**:
```json
{
  "operation": "import_config",
  "status": "completed",
  "total_items": 57,
  "successful": 55,
  "failed": 2,
  "dry_run": true,
  "results": [
    {
      "resource_type": "proxy_host",
      "action": "create",
      "status": "success",
      "details": {
        "domain_names": ["new.example.com"]
      }
    },
    {
      "resource_type": "certificate",
      "action": "create",
      "status": "error",
      "error": "Certificate already exists for domain"
    }
  ],
  "duration_seconds": 15.3
}
```

**Example Usage**:
> "Import configuration from backup.json using merge strategy (dry run first)"

> "Import and replace all configuration from production to staging"

> "Import only proxy hosts from exported config"

---

### Bulk Operations: Advanced Features

#### Concurrent Processing

All bulk operations support concurrent execution with configurable batch size:
```json
{
  "batch_size": 10    // Process 10 items simultaneously (default)
}
```

**Recommendations**:
- Small instances: batch_size=5-10
- Medium instances: batch_size=10-20
- Large instances: batch_size=20-50
- Maximum: 50 (API rate limit protection)

#### Error Resilience

By default, bulk operations continue processing even if individual items fail:
```json
{
  "continue_on_error": true  // Default: true
}
```

**Behavior**:
- Each item result is tracked independently
- Failures don't stop processing
- Detailed error messages for each failure
- Summary includes success_count and failure_count

Set to `false` for fail-fast behavior (stop on first error).

#### Dry-Run Mode

Preview changes before executing (available for all operations):
```json
{
  "dry_run": true  // Default: false
}
```

**Behavior**:
- Validates all parameters and resources
- Checks current state of resources
- Returns preview of changes
- Does NOT execute mutations
- Recommended for delete and replace operations

#### Advanced Filtering

Select resources using query filters instead of explicit IDs:

**Certificate Expiration Filter**:
```json
{
  "operation": "renew_certificates",
  "filters": {
    "expiring_within_days": 30  // Certs expiring in < 30 days
  }
}
```

**Domain Pattern Filter** (substring match):
```json
{
  "operation": "toggle_hosts",
  "filters": {
    "domain_pattern": "staging"  // Matches "*.staging.*", "staging.*", etc.
  }
}
```

**Enabled Status Filter**:
```json
{
  "operation": "toggle_hosts",
  "action": "disable",
  "filters": {
    "enabled_only": true  // Only select currently enabled hosts
  }
}
```

---

## 10. Cross-Instance Operations

### 10.1 `npm_sync_configuration`

**Purpose**: Sync configuration from one instance to another

**Parameters**:
```json
{
  "source_instance": "production",
  "target_instance": "staging",
  "resources": ["proxy_hosts", "certificates", "access_lists"],
  "mode": "mirror",                        // mirror|merge
  "dry_run": true
}
```

**Returns**:
```json
{
  "success": true,
  "source_instance": "production",
  "target_instance": "staging",
  "dry_run": true,
  "sync_plan": {
    "proxy_hosts": {
      "to_create": 10,
      "to_update": 5,
      "to_delete": 2
    },
    "certificates": {
      "to_create": 3,
      "to_update": 1,
      "to_delete": 0
    }
  }
}
```

**Example Usage**:
> "Sync proxy hosts and certificates from production to staging with a dry run"

---

## Tool Usage Tips

### Best Practices

1. **Instance Selection**: Always specify `instance_name` explicitly in automation to avoid ambiguity
2. **Dry Run Mode**: Use dry-run mode for bulk operations to preview changes
3. **Error Handling**: Check the `success` field in responses and handle errors appropriately
4. **Validation**: Use validation tools (like `npm_validate_certificate`) before creating resources
5. **Bulk Operations**: Prefer bulk tools for multiple operations to reduce API calls

### Common Workflows

#### Setting Up a New Proxy Host with SSL
```
1. npm_manage_certificate (create Let's Encrypt cert)
2. npm_manage_proxy_host (create proxy host with cert_id)
3. npm_get_proxy_host (verify configuration)
```

#### Managing Certificate Renewals
```
1. npm_list_certificates (filter expiring_soon: true)
2. npm_bulk_update_certificates (renew expiring certificates)
```

#### Multi-Instance Deployment
```
1. npm_export_configuration (from production)
2. npm_import_configuration (to staging, dry_run: true)
3. Review and approve
4. npm_import_configuration (to staging, dry_run: false)
```

#### Access Control Setup
```
1. npm_manage_access_list (create access list)
2. npm_manage_proxy_host (update host with access_list_id)
```

---

## Error Handling

All tools return structured error responses:

```json
{
  "success": false,
  "error": {
    "code": "AUTHENTICATION_FAILED",
    "message": "Invalid credentials for instance 'production'",
    "details": {
      "instance": "production",
      "status_code": 401
    },
    "suggestions": [
      "Verify username and password in configuration",
      "Test connection using npm_test_connection",
      "Check if API token has expired"
    ]
  }
}
```

### Common Error Codes

- `AUTHENTICATION_FAILED`: Invalid credentials
- `CONNECTION_FAILED`: Cannot reach NPM instance
- `VALIDATION_ERROR`: Invalid parameters
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `RESOURCE_CONFLICT`: Resource already exists or conflicts
- `PERMISSION_DENIED`: Insufficient permissions
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: NPM server error

---

**Last Updated**: 2025-10-26
**Version**: 1.0
