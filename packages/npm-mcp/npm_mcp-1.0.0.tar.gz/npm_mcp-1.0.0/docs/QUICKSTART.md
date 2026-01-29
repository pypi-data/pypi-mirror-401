# Quick Start Guide

Get up and running with npm-mcp in 5 minutes.

## Prerequisites

- Python 3.11 or higher
- An Nginx Proxy Manager instance with API access
- NPM admin credentials

## Installation

```bash
pip install npm-mcp
```

## Configuration

### Option 1: Environment Variables (Simplest)

```bash
export NPM_HOST="npm.example.com"
export NPM_PORT="81"
export NPM_USERNAME="admin@example.com"
export NPM_PASSWORD="your-password"
export NPM_USE_HTTPS="true"
```

### Option 2: Configuration File

Create `~/.config/npm-mcp/instances.yaml`:

```yaml
instances:
  default:
    host: npm.example.com
    port: 81
    use_https: true
    username: admin@example.com
    password: ${NPM_PASSWORD}  # Reference environment variable

default_instance: default
```

## Running the Server

### Standalone Mode

```bash
npm-mcp
```

### With Claude Desktop

Add to your Claude Desktop config (`~/.config/claude/config.json`):

```json
{
  "mcpServers": {
    "npm": {
      "command": "npm-mcp",
      "env": {
        "NPM_HOST": "npm.example.com",
        "NPM_PORT": "81",
        "NPM_USERNAME": "admin@example.com",
        "NPM_PASSWORD": "your-password",
        "NPM_USE_HTTPS": "true"
      }
    }
  }
}
```

## First Commands

Once connected, try these commands in your LLM:

### List Proxy Hosts
> "Show me all proxy hosts"

### Create a Proxy Host
> "Create a proxy host for api.example.com forwarding to 192.168.1.100:3000"

### List SSL Certificates
> "What SSL certificates are configured?"

### Check Certificate Expiration
> "Which certificates are expiring in the next 30 days?"

## Available Tools

npm-mcp provides 28 tools across these categories:

| Category | Tools |
|----------|-------|
| Instance Management | `npm_list_instances`, `npm_manage_instance`, `npm_select_instance` |
| Proxy Hosts | `npm_list_proxy_hosts`, `npm_get_proxy_host`, `npm_manage_proxy_host` |
| SSL Certificates | `npm_list_certificates`, `npm_manage_certificate`, `npm_validate_certificate` |
| Access Lists | `npm_list_access_lists`, `npm_manage_access_list` |
| Streams | `npm_list_streams`, `npm_manage_stream` |
| Redirections | `npm_list_redirections`, `npm_manage_redirection` |
| Dead Hosts | `npm_list_dead_hosts`, `npm_manage_dead_host` |
| Users | `npm_list_users`, `npm_manage_user` |
| System | `npm_get_system_settings`, `npm_update_system_settings`, `npm_get_audit_logs`, `npm_get_host_reports` |
| Bulk Operations | `npm_bulk_operations` |

## Next Steps

- [Full Documentation](README.md)
- [Tool Catalog](TOOL_CATALOG.md) - Detailed reference for all 28 tools
- [Configuration Guide](CONFIGURATION.md) - Advanced configuration options
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
