# Product Requirements Document: Nginx Proxy Manager MCP Server

**Version:** 1.1
**Date:** 2025-10-26 (Updated: 2025-10-26)
**Author:** System Architecture Team
**Status:** Draft

## Changelog

### Version 1.1 (2025-10-26)
- **Enhanced Instance Management**: Expanded from 4 to 7 tools
  - Added `npm_get_instance` - Get detailed instance configuration
  - Added `npm_update_instance_credentials` - Rotate credentials
  - Added `npm_validate_instance_config` - Pre-flight validation
  - Added `npm_set_default_instance` - Change default instance
  - Enhanced `npm_manage_instance` with full CRUD operations
  - Enhanced `npm_list_instances` with filtering capabilities
  - Added `persist_to_file` parameter for configuration persistence
- **Tool Count**: Increased from 25 to 28 semantic tools
- **Capability**: LLMs can now fully manage instance configurations dynamically

### Version 1.0 (2025-10-26)
- Initial PRD with complete NPM API analysis
- 25 semantic tools across 10 categories
- Multi-instance architecture design
- Authentication and security strategy
- 10-week implementation roadmap

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview](#2-project-overview)
3. [Background & Motivation](#3-background--motivation)
4. [Nginx Proxy Manager Capabilities](#4-nginx-proxy-manager-capabilities)
5. [API Endpoint Analysis](#5-api-endpoint-analysis)
6. [MCP Server Architecture](#6-mcp-server-architecture)
7. [Tool Design Philosophy](#7-tool-design-philosophy)
8. [Multi-Instance Management](#8-multi-instance-management)
9. [Authentication & Security](#9-authentication--security)
10. [Technical Implementation Plan](#10-technical-implementation-plan)
11. [Success Metrics](#11-success-metrics)
12. [Future Enhancements](#12-future-enhancements)

---

## 1. Executive Summary

This document outlines the requirements for building a comprehensive Model Context Protocol (MCP) server that enables Large Language Models (LLMs) to manage Nginx Proxy Manager (NPM) instances. The MCP server will provide full-featured access to all NPM API capabilities, support multiple NPM instance management, and follow 2025 MCP best practices.

### Key Objectives

- **Full API Coverage**: Implement all NPM API endpoints (proxy hosts, certificates, access lists, streams, redirections, users, etc.)
- **Multi-Instance Support**: Enable management of multiple NPM instances with configurable credentials
- **Dynamic Instance Management**: Full CRUD operations on instance configurations with persistent storage support
- **LLM-Optimized Tool Design**: Group related operations into semantic tools following MCP best practices
- **Production-Ready Security**: Implement secure authentication, credential management, and authorization flows
- **Python-Based Implementation**: Leverage the official MCP Python SDK for robust implementation

---

## 2. Project Overview

### 2.1 Product Vision

Create a production-ready MCP server that allows AI assistants to seamlessly manage Nginx Proxy Manager deployments through natural language interactions, enabling automated reverse proxy configuration, SSL certificate management, and access control administration.

### 2.2 Target Users

- **DevOps Engineers**: Managing multiple self-hosted services requiring reverse proxy configuration
- **System Administrators**: Overseeing home lab or small business infrastructure
- **AI-Powered Automation**: Enabling autonomous management of web service exposure and SSL certificates

### 2.3 Core Requirements

1. Support all NPM API operations
2. Handle multiple NPM instances simultaneously
3. Secure credential storage and management
4. Semantic tool grouping for LLM efficiency
5. Comprehensive error handling and validation
6. Detailed logging and audit capabilities

---

## 3. Background & Motivation

### 3.1 Nginx Proxy Manager Overview

Nginx Proxy Manager (NPM) is a Docker-based application that simplifies reverse proxying with SSL termination. It provides:

- **Web-Based Admin Interface**: Built on the Tabler framework
- **Easy Proxy Configuration**: Create forwarding domains without deep Nginx knowledge
- **Free SSL Certificates**: Automatic Let's Encrypt integration
- **Access Control**: IP-based access lists and HTTP authentication
- **Stream Proxying**: TCP/UDP stream forwarding capabilities
- **Advanced Configuration**: Custom Nginx config for power users

### 3.2 Why MCP Integration?

**Problem Statement**: Managing multiple NPM instances requires manual interaction through web UIs or direct API calls, making automation difficult and time-consuming.

**Solution**: An MCP server enables:
- Natural language proxy configuration ("Create a proxy host for api.example.com pointing to 192.168.1.100:3000")
- Automated SSL certificate renewal management
- Bulk operations across multiple instances
- Intelligent error handling and troubleshooting
- Integration with AI-powered DevOps workflows

### 3.3 MCP Best Practices (2025)

Based on industry standards and Anthropic's recommendations:

1. **Avoid 1:1 API-to-Tool Mapping**: Group related operations into higher-level semantic tools
2. **Schema Validation**: Use structured outputs with JSON schema validation
3. **Clear Documentation**: Provide comprehensive tool descriptions and examples
4. **Logging & Debugging**: Enable detailed logging for troubleshooting
5. **Security First**: Implement explicit consent flows and secure credential handling
6. **Containerization**: Support Docker deployment for consistency

---

## 4. Nginx Proxy Manager Capabilities

### 4.1 Core Features

#### 4.1.1 Proxy Host Management
- Forward domains to internal services
- Support for multiple domain names per host
- HTTP/HTTPS forwarding schemes
- Configurable forwarding ports (1-65535)
- WebSocket support
- HTTP/2 support
- Caching capabilities
- Custom location-based routing
- Advanced Nginx configuration

#### 4.1.2 SSL Certificate Management
- Let's Encrypt automatic certificate generation
- Custom SSL certificate upload
- DNS challenge support for wildcard certificates
- Certificate renewal automation
- Multiple domain support (up to 100 per certificate)
- Certificate expiration tracking

#### 4.1.3 Access Control
- IP-based access lists (IPv4/IPv6 with CIDR notation)
- Allow/Deny directives
- HTTP Basic authentication
- Access list assignment to proxy hosts
- Satisfy-any vs satisfy-all logic

#### 4.1.4 Stream Proxying
- TCP/UDP stream forwarding
- Port-based routing (1-65535)
- Optional SSL termination for streams
- Enable/disable per stream

#### 4.1.5 Redirection Hosts
- URL redirection management
- Custom HTTP status codes
- Domain-based redirects
- Advanced configuration options

#### 4.1.6 Dead Hosts
- 404 handler configuration
- Catch-all proxy handling
- Custom error pages

#### 4.1.7 User Management
- Multi-user support
- Role-based permissions
- User authentication
- API token generation
- Audit logging of user actions

### 4.2 System Administration

- **Settings Management**: Global system configuration
- **Audit Logs**: Complete activity tracking
- **Reports**: Host performance metrics
- **Health Monitoring**: System health status

---

## 5. API Endpoint Analysis

### 5.1 Complete API Specification

The NPM API (v2.x.x) operates at `http://{host}:81/api` and uses JWT bearer token authentication.

### 5.2 Authentication Endpoints

| Method | Endpoint | Purpose | Request Body |
|--------|----------|---------|--------------|
| POST | `/api/tokens` | User login / Generate JWT token | `{"identity": "email", "secret": "password", "expiry": "10y"}` |
| GET | `/api/tokens` | List API tokens | - |
| DELETE | `/api/tokens/{tokenID}` | Revoke token | - |

**Response**: Returns JWT token for Authorization header: `Authorization: Bearer {token}`

### 5.3 Proxy Host Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/nginx/proxy-hosts` | List all proxy hosts | Query filters, pagination |
| GET | `/api/nginx/proxy-hosts/{hostID}` | Get specific host | - |
| POST | `/api/nginx/proxy-hosts` | Create proxy host | Complete host configuration |
| PUT | `/api/nginx/proxy-hosts/{hostID}` | Update proxy host | Partial or complete update |
| DELETE | `/api/nginx/proxy-hosts/{hostID}` | Delete proxy host | - |
| POST | `/api/nginx/proxy-hosts/{hostID}/enable` | Enable host | - |
| POST | `/api/nginx/proxy-hosts/{hostID}/disable` | Disable host | - |

**Proxy Host Schema** (21 required fields):
```json
{
  "domain_names": ["example.com", "www.example.com"],
  "forward_scheme": "http",
  "forward_host": "192.168.1.100",
  "forward_port": 3000,
  "certificate_id": 1,
  "ssl_forced": true,
  "hsts_enabled": true,
  "hsts_subdomains": false,
  "http2_support": true,
  "block_exploits": true,
  "caching_enabled": false,
  "allow_websocket_upgrade": true,
  "access_list_id": 0,
  "advanced_config": "",
  "enabled": true,
  "meta": {},
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

### 5.4 Certificate Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/nginx/certificates` | List certificates | - |
| GET | `/api/nginx/certificates/{certID}` | Get certificate details | - |
| POST | `/api/nginx/certificates` | Create/request certificate | Provider, domains, validation method |
| PUT | `/api/nginx/certificates/{certID}` | Update certificate | - |
| DELETE | `/api/nginx/certificates/{certID}` | Delete certificate | - |
| POST | `/api/nginx/certificates/{certID}/renew` | Renew certificate | - |
| POST | `/api/nginx/certificates/validate` | Validate certificate configuration | - |
| POST | `/api/nginx/certificates/test-http` | Test HTTP validation | - |
| POST | `/api/nginx/certificates/{certID}/download` | Download certificate files | - |

**Certificate Schema**:
```json
{
  "provider": "letsencrypt",
  "nice_name": "Example Certificate",
  "domain_names": ["example.com", "*.example.com"],
  "meta": {
    "letsencrypt_email": "admin@example.com",
    "letsencrypt_agree": true,
    "dns_challenge": true,
    "dns_provider": "cloudflare",
    "dns_provider_credentials": "credentials_string",
    "propagation_seconds": 60
  }
}
```

### 5.5 Access List Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/nginx/access-lists` | List access lists | - |
| GET | `/api/nginx/access-lists/{listID}` | Get access list | - |
| POST | `/api/nginx/access-lists` | Create access list | Name, directive, addresses |
| PUT | `/api/nginx/access-lists/{listID}` | Update access list | - |
| DELETE | `/api/nginx/access-lists/{listID}` | Delete access list | - |

**Access List Schema**:
```json
{
  "name": "Office Network",
  "directive": "allow",
  "address": "192.168.1.0/24",
  "satisfy_any": true,
  "pass_auth": false,
  "meta": {}
}
```

### 5.6 Stream Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/nginx/streams` | List streams | - |
| GET | `/api/nginx/streams/{streamID}` | Get stream | - |
| POST | `/api/nginx/streams` | Create stream | Ports, forwarding config |
| PUT | `/api/nginx/streams/{streamID}` | Update stream | - |
| DELETE | `/api/nginx/streams/{streamID}` | Delete stream | - |
| POST | `/api/nginx/streams/{streamID}/enable` | Enable stream | - |
| POST | `/api/nginx/streams/{streamID}/disable` | Disable stream | - |

**Stream Schema**:
```json
{
  "incoming_port": 3306,
  "forwarding_host": "192.168.1.50",
  "forwarding_port": 3306,
  "tcp_forwarding": true,
  "udp_forwarding": false,
  "enabled": true,
  "meta": {}
}
```

### 5.7 Redirection Host Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/nginx/redirection-hosts` | List redirections | - |
| GET | `/api/nginx/redirection-hosts/{hostID}` | Get redirection | - |
| POST | `/api/nginx/redirection-hosts` | Create redirection | Source, target, status code |
| PUT | `/api/nginx/redirection-hosts/{hostID}` | Update redirection | - |
| DELETE | `/api/nginx/redirection-hosts/{hostID}` | Delete redirection | - |

### 5.8 Dead Host Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/nginx/dead-hosts` | List dead hosts | - |
| GET | `/api/nginx/dead-hosts/{hostID}` | Get dead host | - |
| POST | `/api/nginx/dead-hosts` | Create dead host | Domain configuration |
| PUT | `/api/nginx/dead-hosts/{hostID}` | Update dead host | - |
| DELETE | `/api/nginx/dead-hosts/{hostID}` | Delete dead host | - |

### 5.9 User Management Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/users` | List users | - |
| GET | `/api/users/{userID}` | Get user details | - |
| POST | `/api/users` | Create user | Email, name, password, permissions |
| PUT | `/api/users/{userID}` | Update user | - |
| DELETE | `/api/users/{userID}` | Delete user | - |
| PUT | `/api/users/{userID}/password` | Change password | Current and new password |
| PUT | `/api/users/{userID}/permissions` | Update permissions | Permission flags |

### 5.10 System Endpoints

| Method | Endpoint | Purpose | Key Parameters |
|--------|----------|---------|----------------|
| GET | `/api/settings` | Get system settings | - |
| PUT | `/api/settings` | Update settings | Settings object |
| GET | `/api/audit-log` | Get audit logs | Query filters, pagination |
| GET | `/api/reports/hosts` | Get host reports | Time range, filters |
| GET | `/api/schema` | Get API schema | - |

---

## 6. MCP Server Architecture

### 6.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         LLM Client                           │
│                    (Claude, ChatGPT, etc.)                   │
└──────────────────────────────┬──────────────────────────────┘
                               │ MCP Protocol
┌──────────────────────────────▼──────────────────────────────┐
│                    MCP Server (Python)                       │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Tool Registry & Router                    │  │
│  │  - Proxy Host Tools                                    │  │
│  │  - Certificate Tools                                   │  │
│  │  - Access List Tools                                   │  │
│  │  - Stream Tools                                        │  │
│  │  - User Management Tools                               │  │
│  │  - System Tools                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │        Instance Configuration Manager                  │  │
│  │  - Multi-instance registry                             │  │
│  │  - Credential management                               │  │
│  │  - Connection pooling                                  │  │
│  │  - Instance selection logic                            │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Authentication & Session Manager               │  │
│  │  - JWT token management                                │  │
│  │  - Token refresh logic                                 │  │
│  │  - Session persistence                                 │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              NPM API Client Layer                      │  │
│  │  - HTTP client (httpx)                                 │  │
│  │  - Request/response handling                           │  │
│  │  - Error handling & retry logic                        │  │
│  │  - Response validation                                 │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │          Validation & Schema Layer                     │  │
│  │  - Pydantic models for all NPM objects                │  │
│  │  - Input validation                                    │  │
│  │  - Output schema enforcement                           │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           Logging & Audit System                       │  │
│  │  - Structured logging                                  │  │
│  │  - Operation audit trail                               │  │
│  │  - Error tracking                                      │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP/REST
┌──────────────────────────────▼──────────────────────────────┐
│              NPM Instance(s) API (Port 81)                   │
│  - Instance A: https://npm1.example.com:81                   │
│  - Instance B: https://npm2.example.com:81                   │
│  - Instance N: https://npmN.example.com:81                   │
└──────────────────────────────────────────────────────────────┘
```

### 6.2 Component Breakdown

#### 6.2.1 MCP Server Core
- Built on official `mcp` Python SDK
- Implements MCP protocol specification (2025-06-18 revision)
- Handles tool registration, discovery, and execution
- Manages server lifecycle and connection handling

#### 6.2.2 Tool Registry & Router
- Registers all MCP tools with proper schemas
- Routes tool invocations to appropriate handlers
- Validates tool inputs against schemas
- Returns structured outputs

#### 6.2.3 Instance Configuration Manager
- Loads NPM instance configurations from file/environment
- Manages multiple instance credentials securely
- Provides instance selection mechanism
- Maintains connection pools per instance

#### 6.2.4 Authentication & Session Manager
- Handles JWT token acquisition via `/api/tokens`
- Manages token lifecycle and expiration
- Implements token refresh logic
- Caches tokens per instance
- Secure credential storage

#### 6.2.5 NPM API Client
- HTTP client using `httpx` (async support)
- Request builder with proper headers
- Response parser and error handler
- Retry logic with exponential backoff
- Rate limiting support

#### 6.2.6 Validation & Schema Layer
- Pydantic models for all NPM objects
- Automatic validation of inputs/outputs
- Type safety throughout the codebase
- JSON schema generation for MCP tools

#### 6.2.7 Logging & Audit System
- Structured logging using Python's `logging` module
- Operation-level audit trails
- Error tracking and reporting
- Debug mode for development

---

## 7. Tool Design Philosophy

### 7.1 Design Principles

Following MCP best practices for 2025, the tool design emphasizes:

1. **Semantic Grouping Over 1:1 Mapping**: Instead of creating 50+ tools (one per endpoint), group related operations into meaningful semantic tools
2. **Context-Aware Operations**: Tools should understand the current state and provide intelligent defaults
3. **Comprehensive Error Messages**: Return actionable error messages with suggestions
4. **Structured Outputs**: Use JSON schema validation for all outputs
5. **Documentation Excellence**: Clear descriptions, examples, and parameter guidance

### 7.2 Proposed Tool Structure

#### 7.2.1 Instance Management Tools (7 tools - Enhanced with Full CRUD)

**Design Note**: Instance management supports full CRUD operations via LLM, allowing dynamic configuration without manual file editing. Supports both in-memory (temporary) and persistent (saved to YAML) configurations.

**Tool: `npm_manage_instance`** (Enhanced from `npm_configure_instance`)
- **Purpose**: Full CRUD operations on NPM instance configurations
- **Operations**: "create" | "update" | "delete" | "test"
- **Parameters**:
  - `operation`: string (required)
  - `instance_name`: string (required)
  - `host`: string (required for create)
  - `port`: integer (1-65535, optional, default: 81)
  - `use_https`: boolean (optional, default: false)
  - `verify_ssl`: boolean (optional, default: true)
  - `username`: string (required if not using api_token)
  - `password`: string (required if not using api_token)
  - `api_token`: string (alternative to username/password)
  - `set_as_default`: boolean (optional, default: false)
  - `persist_to_file`: boolean (optional, default: false) - **NEW: Save to YAML**
  - `config_file`: string (optional, default: ~/.npm-mcp/instances.yaml)
  - `description`: string (optional)
  - `tags`: array of strings (optional)
  - `test_connection`: boolean (optional, default: true for create)
  - `timeout`: integer (optional, default: 30)
- **Returns**: Instance configuration with connection status and persistence confirmation
- **Example**: "Add NPM instance 'homelab' at 192.168.1.100 with admin@local/password and save to config"

**Tool: `npm_get_instance`** (NEW)
- **Purpose**: Get detailed configuration for a specific instance
- **Parameters**:
  - `instance_name`: string (required)
  - `show_credentials`: boolean (optional, default: false) - Show masked credentials
- **Returns**: Complete instance configuration with connection status, credentials (masked), token status, and persistence info
- **Example**: "Show me the configuration for the production instance"

**Tool: `npm_list_instances`** (Enhanced)
- **Purpose**: List all configured NPM instances with filtering
- **Parameters**:
  - `filter_tags`: array of strings (optional) - **NEW: Filter by tags**
  - `filter_connected`: boolean (optional) - **NEW: Only show connected instances**
  - `show_credentials`: boolean (optional, default: false) - Show masked credentials
  - `include_test_results`: boolean (optional, default: false) - Include last connection test
- **Returns**: Array of instance configurations with connection status
- **Example**: "List all connected NPM instances"

**Tool: `npm_select_instance`**
- **Purpose**: Set the active instance for subsequent operations
- **Parameters**:
  - `instance_name`: string (required)
  - `test_connection`: boolean (optional, default: true) - Test before selecting
- **Returns**: Selected instance details with connection confirmation
- **Example**: "Switch to the staging instance"

**Tool: `npm_update_instance_credentials`** (NEW)
- **Purpose**: Rotate credentials without recreating instance
- **Parameters**:
  - `instance_name`: string (required)
  - `new_username`: string (optional)
  - `new_password`: string (optional)
  - `new_api_token`: string (optional, alternative to username/password)
  - `test_before_applying`: boolean (optional, default: true) - Test new credentials first
  - `persist_to_file`: boolean (optional, default: false) - Update config file
  - `invalidate_cached_tokens`: boolean (optional, default: true) - Clear old JWT tokens
- **Returns**: Credential update confirmation with test results
- **Example**: "Update the production instance password to 'newpass456' and save it"

**Tool: `npm_validate_instance_config`** (NEW)
- **Purpose**: Validate instance configuration before adding (pre-flight check)
- **Parameters**: Same as `npm_manage_instance` create operation
- **Returns**: Validation results with detailed checks:
  - Host reachability
  - Port accessibility
  - SSL certificate validation
  - Authentication success
  - API version detection
  - Network latency
- **Example**: "Validate this NPM configuration before I add it"

**Tool: `npm_set_default_instance`** (NEW)
- **Purpose**: Change which instance is the default
- **Parameters**:
  - `instance_name`: string (required)
  - `persist_to_file`: boolean (optional, default: false) - Update config file
- **Returns**: Confirmation with previous and new default instance
- **Example**: "Make the homelab instance the default"

#### 7.2.2 Proxy Host Management Tools

**Tool: `npm_manage_proxy_host`**
- **Purpose**: Create, update, or delete proxy hosts (unified interface)
- **Parameters**:
  - `operation`: "create" | "update" | "delete" | "enable" | "disable"
  - `host_id`: number (required for update/delete/enable/disable)
  - `domain_names`: array of strings
  - `forward_host`: string
  - `forward_port`: integer
  - `forward_scheme`: "http" | "https"
  - `ssl_certificate_id`: integer (optional)
  - `force_ssl`: boolean
  - `http2_support`: boolean
  - `websocket_support`: boolean
  - `block_exploits`: boolean
  - `caching_enabled`: boolean
  - `access_list_id`: integer (optional)
  - `locations`: array of location objects (optional)
  - `advanced_config`: string (optional)
- **Returns**: Proxy host object with all details

**Tool: `npm_list_proxy_hosts`**
- **Purpose**: List all proxy hosts with filtering
- **Parameters**:
  - `domain_filter`: string (optional)
  - `enabled_only`: boolean (optional)
  - `page`: integer (optional)
  - `limit`: integer (optional)
- **Returns**: Array of proxy host objects

**Tool: `npm_get_proxy_host`**
- **Purpose**: Get detailed information about a specific proxy host
- **Parameters**:
  - `host_id`: integer OR `domain_name`: string
- **Returns**: Complete proxy host object with relationships

#### 7.2.3 Certificate Management Tools

**Tool: `npm_manage_certificate`**
- **Purpose**: Create, update, delete, or renew certificates
- **Parameters**:
  - `operation`: "create" | "update" | "delete" | "renew"
  - `cert_id`: integer (required for update/delete/renew)
  - `provider`: "letsencrypt" | "custom"
  - `nice_name`: string
  - `domain_names`: array of strings
  - `letsencrypt_email`: string (for Let's Encrypt)
  - `dns_challenge`: boolean
  - `dns_provider`: string (e.g., "cloudflare", "route53")
  - `dns_credentials`: string (for DNS challenge)
  - `custom_certificate`: string (PEM format, for custom certs)
  - `custom_key`: string (PEM format, for custom certs)
- **Returns**: Certificate object with expiration details

**Tool: `npm_list_certificates`**
- **Purpose**: List all certificates with expiration tracking
- **Parameters**:
  - `expiring_soon`: boolean (filter certs expiring in < 30 days)
  - `provider`: string (filter by provider)
- **Returns**: Array of certificate objects

**Tool: `npm_validate_certificate`**
- **Purpose**: Validate certificate configuration before creation
- **Parameters**: Same as certificate creation
- **Returns**: Validation result with any errors/warnings

#### 7.2.4 Access Control Tools

**Tool: `npm_manage_access_list`**
- **Purpose**: Create, update, or delete access lists
- **Parameters**:
  - `operation`: "create" | "update" | "delete"
  - `list_id`: integer (required for update/delete)
  - `name`: string
  - `directive`: "allow" | "deny"
  - `addresses`: array of IP/CIDR strings
  - `satisfy_any`: boolean
  - `pass_auth`: boolean
  - `clients`: array of client objects (username/password for basic auth)
- **Returns**: Access list object

**Tool: `npm_list_access_lists`**
- **Purpose**: List all access lists
- **Returns**: Array of access list objects

#### 7.2.5 Stream Management Tools

**Tool: `npm_manage_stream`**
- **Purpose**: Create, update, delete, or toggle streams
- **Parameters**:
  - `operation`: "create" | "update" | "delete" | "enable" | "disable"
  - `stream_id`: integer (required for update/delete/enable/disable)
  - `incoming_port`: integer
  - `forwarding_host`: string
  - `forwarding_port`: integer
  - `tcp_forwarding`: boolean
  - `udp_forwarding`: boolean
  - `certificate_id`: integer (optional, for SSL)
- **Returns**: Stream object

**Tool: `npm_list_streams`**
- **Purpose**: List all streams
- **Parameters**:
  - `enabled_only`: boolean (optional)
- **Returns**: Array of stream objects

#### 7.2.6 Redirection & Dead Host Tools

**Tool: `npm_manage_redirection`**
- **Purpose**: Manage URL redirections
- **Parameters**:
  - `operation`: "create" | "update" | "delete"
  - `redirect_id`: integer (required for update/delete)
  - `domain_names`: array of strings
  - `forward_scheme`: string
  - `forward_domain_name`: string
  - `preserve_path`: boolean
  - `certificate_id`: integer (optional)
- **Returns**: Redirection object

**Tool: `npm_manage_dead_host`**
- **Purpose**: Manage 404/dead hosts
- **Parameters**:
  - `operation`: "create" | "update" | "delete"
  - `host_id`: integer (required for update/delete)
  - `domain_names`: array of strings
  - `certificate_id`: integer (optional)
- **Returns**: Dead host object

#### 7.2.7 User Management Tools

**Tool: `npm_manage_user`**
- **Purpose**: Create, update, or delete users
- **Parameters**:
  - `operation`: "create" | "update" | "delete" | "change_password"
  - `user_id`: integer (required for update/delete/change_password)
  - `name`: string
  - `email`: string
  - `password`: string
  - `is_admin`: boolean
  - `permissions`: object (granular permissions)
- **Returns**: User object (password masked)

**Tool: `npm_list_users`**
- **Purpose**: List all users
- **Returns**: Array of user objects

#### 7.2.8 System & Reporting Tools

**Tool: `npm_get_system_settings`**
- **Purpose**: Get current system settings
- **Returns**: Settings object

**Tool: `npm_update_system_settings`**
- **Purpose**: Update system settings
- **Parameters**: Settings object
- **Returns**: Updated settings

**Tool: `npm_get_audit_logs`**
- **Purpose**: Retrieve audit logs
- **Parameters**:
  - `start_date`: date (optional)
  - `end_date`: date (optional)
  - `user_id`: integer (optional)
  - `action_filter`: string (optional)
  - `page`: integer
  - `limit`: integer
- **Returns**: Array of audit log entries

**Tool: `npm_get_host_reports`**
- **Purpose**: Get performance reports for hosts
- **Parameters**:
  - `time_range`: string ("1h" | "24h" | "7d" | "30d")
  - `host_ids`: array of integers (optional)
- **Returns**: Report data with metrics

#### 7.2.9 Bulk Operations Tools

**Tool: `npm_bulk_update_certificates`**
- **Purpose**: Update or renew multiple certificates
- **Parameters**:
  - `cert_ids`: array of integers OR `renew_expiring`: boolean
  - `operation`: "renew" | "delete"
- **Returns**: Array of operation results

**Tool: `npm_bulk_toggle_hosts`**
- **Purpose**: Enable or disable multiple proxy hosts
- **Parameters**:
  - `host_ids`: array of integers OR `domain_pattern`: string
  - `action`: "enable" | "disable"
- **Returns**: Array of operation results

**Tool: `npm_export_configuration`**
- **Purpose**: Export entire NPM configuration for backup
- **Returns**: JSON containing all configurations

**Tool: `npm_import_configuration`**
- **Purpose**: Import configuration from backup
- **Parameters**: Configuration JSON
- **Returns**: Import result with success/failure details

### 7.3 Tool Count Summary

**Total Tools**: ~28 semantic tools (vs 50+ if following 1:1 API mapping)

**Tool Categories**:
- Instance Management: 7 tools (Enhanced with full CRUD + persistence)
- Proxy Hosts: 3 tools
- Certificates: 3 tools
- Access Lists: 2 tools
- Streams: 2 tools
- Redirections: 1 tool
- Dead Hosts: 1 tool
- Users: 2 tools
- System & Reporting: 4 tools
- Bulk Operations: 3 tools

**Key Enhancement**: Instance Management expanded from 4 to 7 tools to support full CRUD operations with configuration persistence, enabling LLMs to dynamically manage NPM instance configurations without manual file editing.

This design follows the MCP best practice of "grouping related tasks and designing higher-level functions" rather than creating a tool for every API endpoint.

---

## 8. Multi-Instance Management

### 8.1 Configuration Strategy

#### 8.1.1 Configuration File Format

**Location**: `~/.npm-mcp/instances.yaml` or environment variable `NPM_MCP_CONFIG`

```yaml
instances:
  - name: "production"
    host: "npm.example.com"
    port: 81
    use_https: true
    username: "admin@example.com"
    password: "${NPM_PROD_PASSWORD}"  # Environment variable reference
    default: true

  - name: "homelab"
    host: "192.168.1.100"
    port: 81
    use_https: false
    username: "admin@homelab.local"
    password: "${NPM_HOMELAB_PASSWORD}"
    default: false

  - name: "staging"
    host: "npm-staging.example.com"
    port: 81
    use_https: true
    api_token: "${NPM_STAGING_TOKEN}"  # Pre-generated token
    default: false

# Global settings
settings:
  default_timeout: 30
  retry_attempts: 3
  log_level: "INFO"
  cache_tokens: true
  token_cache_dir: "~/.npm-mcp/tokens"
```

#### 8.1.2 Environment Variable Configuration

For scenarios without config files:

```bash
NPM_INSTANCES='[
  {"name":"prod","host":"npm.example.com","port":81,"username":"admin@example.com","password":"secret123"},
  {"name":"dev","host":"192.168.1.100","port":81,"username":"admin@dev.local","password":"dev456"}
]'
```

#### 8.1.3 Secure Credential Storage

**Options**:
1. **Environment Variables**: For CI/CD and container deployments
2. **Encrypted Config File**: Using `cryptography` library with user-provided key
3. **System Keyring**: Using `keyring` library for OS-level credential storage
4. **Secrets Manager Integration**: AWS Secrets Manager, HashiCorp Vault, etc.

**Recommended Approach**: Hybrid
- Development: Encrypted config file or system keyring
- Production: Environment variables or secrets manager

### 8.2 Instance Selection Logic

#### 8.2.1 Default Instance

- If no instance specified in tool call, use the instance marked `default: true`
- If no default configured, use the first instance in the list
- Log warnings when falling back to defaults

#### 8.2.2 Explicit Instance Selection

All tools accept an optional `instance_name` parameter:

```json
{
  "tool": "npm_manage_proxy_host",
  "arguments": {
    "instance_name": "production",
    "operation": "create",
    "domain_names": ["api.example.com"],
    ...
  }
}
```

#### 8.2.3 Instance Context Persistence

Implement `npm_select_instance` tool to set context for subsequent operations:

```json
{
  "tool": "npm_select_instance",
  "arguments": {
    "instance_name": "staging"
  }
}
```

After this call, all subsequent tool invocations without explicit `instance_name` use "staging" until changed.

### 8.3 Connection Pooling

- Maintain separate HTTP connection pools per instance
- Reuse connections for efficiency
- Implement connection timeouts and cleanup
- Handle connection failures gracefully with retries

### 8.4 Cross-Instance Operations

**Tool: `npm_sync_configuration`**
- **Purpose**: Sync configuration from one instance to another
- **Parameters**:
  - `source_instance`: string
  - `target_instance`: string
  - `resources`: array ["proxy_hosts", "certificates", "access_lists", etc.]
  - `dry_run`: boolean
- **Returns**: Sync plan and results

---

## 9. Authentication & Security

### 9.1 Authentication Flow

#### 9.1.1 Initial Authentication

```
1. MCP Server starts
2. Load instance configurations
3. For each instance:
   a. Check if cached token exists and is valid
   b. If not, authenticate via POST /api/tokens
   c. Store token in memory (and optionally cache to disk)
   d. Set up token refresh timer
```

#### 9.1.2 Token Management

**Token Structure**: JWT with expiration (configurable, e.g., "10y")

**Token Lifecycle**:
- Generate token with long expiration during initial auth
- Cache tokens securely (encrypted if stored to disk)
- Validate token before each request (check expiration)
- Refresh token if expired or near expiration
- Handle 401 responses by re-authenticating

**Token Caching**:
```python
# Token cache structure
{
  "instance_name": {
    "token": "eyJhbGc...",
    "expires_at": "2035-10-26T12:00:00Z",
    "generated_at": "2025-10-26T12:00:00Z",
    "user_id": 1
  }
}
```

#### 9.1.3 Token Refresh Strategy

- Proactive: Refresh tokens that expire within 30 days
- Reactive: Handle 401 errors by re-authenticating
- Fallback: If token refresh fails, re-authenticate with credentials

### 9.2 Credential Security

#### 9.2.1 Storage Security

**Requirements**:
1. Never log credentials in plain text
2. Encrypt config files containing passwords
3. Use OS keyring when possible
4. Support credential rotation without downtime

**Implementation**:
```python
from cryptography.fernet import Fernet
import keyring

# Option 1: Encrypted config file
def encrypt_config(config_data, encryption_key):
    fernet = Fernet(encryption_key)
    encrypted = fernet.encrypt(json.dumps(config_data).encode())
    return encrypted

# Option 2: System keyring
def store_credential(instance_name, username, password):
    keyring.set_password(f"npm-mcp-{instance_name}", username, password)

def get_credential(instance_name, username):
    return keyring.get_password(f"npm-mcp-{instance_name}", username)
```

#### 9.2.2 Credential Rotation

**Tool: `npm_rotate_credentials`**
- Update password/token for an instance
- Re-authenticate automatically
- Update cached tokens
- No service interruption

### 9.3 Authorization & Permissions

#### 9.3.1 NPM User Permissions

NPM supports role-based permissions. The MCP server should:
- Respect NPM user permissions
- Handle 403 errors gracefully with clear messages
- Log authorization failures for audit

#### 9.3.2 MCP-Level Access Control (Optional Future Enhancement)

For multi-user MCP deployments:
- Map MCP users to NPM instances
- Restrict instance access per MCP user
- Audit all operations by user

### 9.4 Security Best Practices

1. **Transport Security**:
   - Always use HTTPS for NPM connections when possible
   - Verify SSL certificates (with option to disable for self-signed in dev)
   - Implement certificate pinning for production

2. **Input Validation**:
   - Validate all inputs against schemas
   - Sanitize strings to prevent injection attacks
   - Limit array sizes and string lengths

3. **Error Handling**:
   - Never expose credentials in error messages
   - Log security events separately
   - Rate limit failed authentication attempts

4. **Audit Logging**:
   - Log all operations with timestamps
   - Include instance name, operation, user, result
   - Store logs securely with rotation

---

## 10. Technical Implementation Plan

### 10.1 Technology Stack

#### 10.1.1 Core Dependencies

```
Python >= 3.11
mcp >= 1.19.0                 # Official MCP SDK
httpx >= 0.28.0               # Async HTTP client
pydantic >= 2.12.0            # Data validation
pyyaml >= 6.0.3               # Config file parsing
cryptography >= 46.0.0        # Encryption
keyring >= 25.6.0             # Credential storage
python-dotenv >= 1.1.0        # Environment variable management
structlog >= 25.4.0           # Structured logging
tenacity >= 9.1.0             # Retry logic
pytest >= 8.4.0               # Testing
pytest-asyncio >= 1.2.0       # Async testing
pytest-cov >= 7.0.0           # Coverage reporting
pytest-mock >= 3.15.0         # Mocking
ruff >= 0.14.0                # Linting and formatting
mypy >= 1.18.0                # Type checking
types-pyyaml >= 6.0.12        # Type stubs for PyYAML
```

### 10.2 Project Structure

```
npm-mcp/
├── pyproject.toml                 # Project metadata and dependencies
├── README.md                      # User documentation
├── docs/
│   ├── PRD.md                     # This document
│   ├── API_REFERENCE.md           # Complete API documentation
│   ├── TOOL_CATALOG.md            # MCP tool documentation
│   └── DEPLOYMENT.md              # Deployment guide
├── src/
│   └── npm_mcp/
│       ├── __init__.py
│       ├── __main__.py            # Entry point
│       ├── server.py              # MCP server implementation
│       ├── config/
│       │   ├── __init__.py
│       │   ├── loader.py          # Config file loader
│       │   ├── models.py          # Config Pydantic models
│       │   └── validation.py      # Config validation
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── manager.py         # Authentication manager
│       │   ├── token_cache.py     # Token caching
│       │   └── credentials.py     # Credential storage
│       ├── client/
│       │   ├── __init__.py
│       │   ├── npm_client.py      # NPM API client
│       │   ├── http_client.py     # HTTP layer
│       │   └── error_handler.py   # Error handling
│       ├── models/
│       │   ├── __init__.py
│       │   ├── proxy_host.py      # Proxy host models
│       │   ├── certificate.py     # Certificate models
│       │   ├── access_list.py     # Access list models
│       │   ├── stream.py          # Stream models
│       │   ├── user.py            # User models
│       │   └── common.py          # Common/shared models
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py            # Base tool class
│       │   ├── instance.py        # Instance management tools
│       │   ├── proxy_host.py      # Proxy host tools
│       │   ├── certificate.py     # Certificate tools
│       │   ├── access_list.py     # Access list tools
│       │   ├── stream.py          # Stream tools
│       │   ├── redirection.py     # Redirection tools
│       │   ├── user.py            # User management tools
│       │   ├── system.py          # System tools
│       │   └── bulk.py            # Bulk operation tools
│       └── utils/
│           ├── __init__.py
│           ├── logging.py         # Logging setup
│           ├── validation.py      # Validation helpers
│           └── helpers.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_config/
│   ├── test_auth/
│   ├── test_client/
│   ├── test_tools/
│   └── test_integration/
├── examples/
│   ├── basic_usage.py
│   ├── multi_instance.py
│   └── bulk_operations.py
└── .npm-mcp/
    └── instances.example.yaml     # Example config
```

### 10.3 Development Phases

#### Phase 1: Foundation (Week 1-2)
- ✅ Project setup and dependencies
- ✅ Configuration system implementation
- ✅ Authentication and token management
- ✅ HTTP client with retry logic
- ✅ Pydantic models for all NPM objects
- ✅ Basic logging setup

**Deliverables**:
- Working config loader
- Authenticated NPM API client
- Complete data models

#### Phase 2: Core Tools (Week 3-4)
- ✅ MCP server setup with official SDK
- ✅ Instance management tools (4 tools)
- ✅ Proxy host management tools (3 tools)
- ✅ Certificate management tools (3 tools)
- ✅ Access list tools (2 tools)
- ✅ Unit tests for core functionality

**Deliverables**:
- Functional MCP server
- 12 core tools working
- Test coverage > 70%

#### Phase 3: Extended Features (Week 5-6)
- ✅ Stream management tools (2 tools)
- ✅ Redirection and dead host tools (2 tools)
- ✅ User management tools (2 tools)
- ✅ System and reporting tools (4 tools)
- ✅ Integration tests

**Deliverables**:
- Complete tool suite (25 tools)
- Integration test suite
- Test coverage > 80%

#### Phase 4: Advanced Features (Week 7-8)
- ✅ Bulk operation tools (3 tools)
- ✅ Cross-instance operations
- ✅ Enhanced error handling
- ✅ Comprehensive logging and audit
- ✅ Performance optimization

**Deliverables**:
- All advanced features
- Performance benchmarks
- Complete documentation

#### Phase 5: Polish & Release (Week 9-10)
- ✅ Documentation completion
- ✅ Example scripts
- ✅ Docker containerization
- ✅ CI/CD pipeline
- ✅ Security audit
- ✅ Release preparation

**Deliverables**:
- Production-ready release
- Published documentation
- Docker image
- PyPI package

### 10.4 Testing Strategy

#### 10.4.1 Unit Tests
- Test all Pydantic models
- Test configuration loading
- Test authentication logic
- Test each tool in isolation (mocked NPM API)
- Target: > 80% code coverage

#### 10.4.2 Integration Tests
- Test against real NPM instance (Docker)
- Test multi-instance scenarios
- Test error handling with failing NPM
- Test token expiration and refresh

#### 10.4.3 End-to-End Tests
- Test complete workflows via MCP protocol
- Test with actual LLM client (Claude Desktop)
- Test bulk operations
- Test cross-instance sync

#### 10.4.4 Security Tests
- Test credential storage security
- Test token handling
- Test input validation
- Test rate limiting
- Penetration testing (optional)

### 10.5 Documentation Requirements

1. **README.md**: Quick start, installation, basic usage
2. **API_REFERENCE.md**: Complete NPM API documentation
3. **TOOL_CATALOG.md**: All MCP tools with examples
4. **DEPLOYMENT.md**: Production deployment guide
5. **CONFIGURATION.md**: Configuration reference
6. **SECURITY.md**: Security best practices
7. **CONTRIBUTING.md**: Development guide

---

## 11. Success Metrics

### 11.1 Functional Metrics

- ✅ **API Coverage**: 100% of NPM API endpoints supported
- ✅ **Tool Count**: ~25 semantic tools implemented
- ✅ **Multi-Instance**: Support for unlimited instances
- ✅ **Error Handling**: Graceful handling of all error scenarios
- ✅ **Test Coverage**: > 80% code coverage

### 11.2 Performance Metrics

- **Response Time**: < 2s for typical operations
- **Bulk Operations**: Handle 100+ items without timeout
- **Connection Pool**: Efficient connection reuse
- **Memory Usage**: < 100MB baseline memory

### 11.3 Quality Metrics

- **Code Quality**: Passes pylint, mypy, ruff checks
- **Security**: No known vulnerabilities
- **Documentation**: 100% of public APIs documented
- **User Satisfaction**: Positive feedback from early adopters

### 11.4 Adoption Metrics

- **GitHub Stars**: Track community interest
- **Issues/PRs**: Active community engagement
- **Downloads**: PyPI download statistics
- **Integration**: Usage in production environments

---

## 12. Future Enhancements

### 12.1 Short-term (3-6 months)

1. **Web UI for Configuration**: Simple web interface for managing instances
2. **Health Monitoring Dashboard**: Real-time monitoring of NPM instances
3. **Automated Backup**: Scheduled configuration backups
4. **Notification System**: Alerts for certificate expiration, failures, etc.
5. **Template System**: Pre-configured templates for common setups

### 12.2 Medium-term (6-12 months)

1. **High Availability**: Support for NPM HA deployments
2. **Git Integration**: Version control for NPM configurations
3. **Terraform Provider**: Generate Terraform configs from NPM
4. **Migration Tools**: Migrate from other reverse proxy solutions
5. **Analytics**: Advanced usage analytics and insights

### 12.3 Long-term (12+ months)

1. **Multi-User MCP Server**: Support multiple concurrent users
2. **Advanced RBAC**: Fine-grained access control
3. **Plugin System**: Extensibility for custom operations
4. **AI-Powered Optimization**: Automatic performance tuning
5. **Cloud Integration**: Direct integration with cloud providers

---

## 13. Risks & Mitigations

### 13.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| NPM API changes | High | Medium | Version detection, backward compatibility |
| Token expiration issues | Medium | Low | Proactive refresh, graceful re-auth |
| Network failures | Medium | Medium | Retry logic, connection pooling |
| Performance bottlenecks | Low | Low | Async operations, caching |

### 13.2 Security Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Credential exposure | High | Low | Encryption, secure storage |
| Unauthorized access | High | Low | Strong authentication, audit logging |
| API abuse | Medium | Low | Rate limiting, validation |
| Token theft | Medium | Low | Secure token storage, expiration |

### 13.3 Operational Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Configuration errors | Medium | Medium | Validation, dry-run mode |
| Multiple instance conflicts | Low | Low | Clear documentation, warnings |
| Downtime during updates | Low | Medium | Graceful degradation, rollback |

---

## 14. Appendices

### Appendix A: NPM API Endpoint Matrix

| Category | Endpoint | Method | Tool Coverage |
|----------|----------|--------|---------------|
| Auth | `/api/tokens` | POST | `npm_test_connection` |
| Auth | `/api/tokens` | GET | `npm_test_connection` |
| Proxy Hosts | `/api/nginx/proxy-hosts` | GET | `npm_list_proxy_hosts` |
| Proxy Hosts | `/api/nginx/proxy-hosts` | POST | `npm_manage_proxy_host` |
| Proxy Hosts | `/api/nginx/proxy-hosts/{id}` | GET | `npm_get_proxy_host` |
| Proxy Hosts | `/api/nginx/proxy-hosts/{id}` | PUT | `npm_manage_proxy_host` |
| Proxy Hosts | `/api/nginx/proxy-hosts/{id}` | DELETE | `npm_manage_proxy_host` |
| Proxy Hosts | `/api/nginx/proxy-hosts/{id}/enable` | POST | `npm_manage_proxy_host` |
| Proxy Hosts | `/api/nginx/proxy-hosts/{id}/disable` | POST | `npm_manage_proxy_host` |
| Certificates | `/api/nginx/certificates` | GET | `npm_list_certificates` |
| Certificates | `/api/nginx/certificates` | POST | `npm_manage_certificate` |
| Certificates | `/api/nginx/certificates/{id}` | GET | `npm_list_certificates` |
| Certificates | `/api/nginx/certificates/{id}` | PUT | `npm_manage_certificate` |
| Certificates | `/api/nginx/certificates/{id}` | DELETE | `npm_manage_certificate` |
| Certificates | `/api/nginx/certificates/{id}/renew` | POST | `npm_manage_certificate` |
| Certificates | `/api/nginx/certificates/validate` | POST | `npm_validate_certificate` |
| Access Lists | `/api/nginx/access-lists` | GET | `npm_list_access_lists` |
| Access Lists | `/api/nginx/access-lists` | POST | `npm_manage_access_list` |
| Access Lists | `/api/nginx/access-lists/{id}` | GET | `npm_list_access_lists` |
| Access Lists | `/api/nginx/access-lists/{id}` | PUT | `npm_manage_access_list` |
| Access Lists | `/api/nginx/access-lists/{id}` | DELETE | `npm_manage_access_list` |
| Streams | `/api/nginx/streams` | GET | `npm_list_streams` |
| Streams | `/api/nginx/streams` | POST | `npm_manage_stream` |
| Streams | `/api/nginx/streams/{id}` | GET | `npm_list_streams` |
| Streams | `/api/nginx/streams/{id}` | PUT | `npm_manage_stream` |
| Streams | `/api/nginx/streams/{id}` | DELETE | `npm_manage_stream` |
| Streams | `/api/nginx/streams/{id}/enable` | POST | `npm_manage_stream` |
| Streams | `/api/nginx/streams/{id}/disable` | POST | `npm_manage_stream` |
| Users | `/api/users` | GET | `npm_list_users` |
| Users | `/api/users` | POST | `npm_manage_user` |
| Users | `/api/users/{id}` | GET | `npm_list_users` |
| Users | `/api/users/{id}` | PUT | `npm_manage_user` |
| Users | `/api/users/{id}` | DELETE | `npm_manage_user` |
| Users | `/api/users/{id}/password` | PUT | `npm_manage_user` |
| System | `/api/settings` | GET | `npm_get_system_settings` |
| System | `/api/settings` | PUT | `npm_update_system_settings` |
| Audit | `/api/audit-log` | GET | `npm_get_audit_logs` |
| Reports | `/api/reports/hosts` | GET | `npm_get_host_reports` |

### Appendix B: Glossary

- **MCP**: Model Context Protocol - Standard for AI-tool integration
- **NPM**: Nginx Proxy Manager - Web-based reverse proxy management
- **JWT**: JSON Web Token - Authentication token format
- **CIDR**: Classless Inter-Domain Routing - IP address notation
- **SSL/TLS**: Secure Socket Layer / Transport Layer Security
- **HSTS**: HTTP Strict Transport Security
- **ACME**: Automatic Certificate Management Environment (Let's Encrypt protocol)

### Appendix C: References

1. [Nginx Proxy Manager Documentation](https://nginxproxymanager.com/guide/)
2. [MCP Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18)
3. [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
4. [MCP Best Practices 2025](https://www.marktechpost.com/2025/07/23/7-mcp-server-best-practices-for-scalable-ai-integrations-in-2025/)
5. [NPM GitHub Repository](https://github.com/NginxProxyManager/nginx-proxy-manager)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-26 | System Architecture | Initial PRD creation |

---

**Document Status**: Draft - Ready for Review

**Next Steps**:
1. Review and approval by stakeholders
2. Technical feasibility assessment
3. Resource allocation
4. Implementation kickoff
