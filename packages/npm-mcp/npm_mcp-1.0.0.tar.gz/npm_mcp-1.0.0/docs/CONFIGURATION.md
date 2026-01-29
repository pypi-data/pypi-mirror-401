# Configuration Guide

This guide provides comprehensive documentation for configuring the NPM MCP Server, including instance management, credential handling, security settings, and advanced options.

## Table of Contents

- [Overview](#overview)
- [Configuration File Structure](#configuration-file-structure)
- [Instance Configuration](#instance-configuration)
- [Credential Management](#credential-management)
- [Global Settings](#global-settings)
- [Environment Variables](#environment-variables)
- [Multi-Instance Setup](#multi-instance-setup)
- [Security Best Practices](#security-best-practices)
- [Advanced Configuration](#advanced-configuration)
- [Configuration Examples](#configuration-examples)

## Overview

The NPM MCP Server uses YAML configuration files for managing NPM instances and global settings. Configuration can be customized using:

1. **YAML Configuration File**: Primary configuration (`instances.yaml`)
2. **Environment Variables**: For sensitive credentials and overrides
3. **System Keyring**: For secure credential storage (recommended for production)
4. **Command-Line Arguments**: For runtime overrides (limited support)

### Configuration File Location

**Default Path**: `~/.npm-mcp/instances.yaml`

**Custom Path**: Set via environment variable:
```bash
export NPM_MCP_CONFIG=/path/to/custom/config.yaml
```

**Precedence Order** (highest to lowest):
1. Environment variables (e.g., `NPM_PASSWORD`)
2. System keyring (if `use_keyring: true`)
3. YAML configuration file
4. Default values

---

## Configuration File Structure

### Basic Structure

```yaml
# instances.yaml

# List of NPM instances to manage
instances:
  - name: production
    host: npm.example.com
    port: 81
    use_https: true
    username: admin
    password: ${NPM_PASSWORD}
    default: true

  - name: staging
    host: npm-staging.example.com
    port: 81
    use_https: true
    username: admin
    password: ${NPM_STAGING_PASSWORD}

# Global server settings
settings:
  timeout: 30
  retry_attempts: 3
  retry_delay: 1.0
  log_level: INFO
  cache_tokens: true
  token_cache_path: ~/.npm-mcp/token_cache
```

---

## Instance Configuration

Each NPM instance requires specific connection and authentication parameters.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier for the instance (alphanumeric, underscores, hyphens) |
| `host` | string | NPM instance hostname or IP address |
| `username` | string | NPM admin username |
| `password` | string | NPM admin password (use environment variables or keyring) |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `port` | integer | 81 | NPM API port |
| `use_https` | boolean | true | Use HTTPS for API connections |
| `verify_ssl` | boolean | true | Verify SSL certificates (set to false for self-signed) |
| `default` | boolean | false | Make this the default instance for operations |
| `use_keyring` | boolean | false | Retrieve password from system keyring |
| `description` | string | null | Human-readable description of the instance |
| `tags` | list | [] | Tags for categorization (e.g., ["production", "us-east"]) |

### Instance Configuration Examples

#### Minimal Configuration

```yaml
instances:
  - name: production
    host: npm.example.com
    username: admin
    password: ${NPM_PASSWORD}
    default: true
```

#### Full Configuration

```yaml
instances:
  - name: production
    host: npm.example.com
    port: 81
    use_https: true
    verify_ssl: true
    username: admin@example.com
    password: ${NPM_PROD_PASSWORD}
    default: true
    description: "Production NPM instance (US East)"
    tags:
      - production
      - us-east
      - critical
```

#### Self-Signed Certificate

```yaml
instances:
  - name: development
    host: npm-dev.local
    port: 81
    use_https: true
    verify_ssl: false  # Disable SSL verification for self-signed certs
    username: admin
    password: ${NPM_DEV_PASSWORD}
```

#### Multiple Instances with Different Regions

```yaml
instances:
  - name: us-east-prod
    host: npm-useast.example.com
    username: admin
    password: ${NPM_USEAST_PASSWORD}
    default: true
    tags: [production, us-east]

  - name: us-west-prod
    host: npm-uswest.example.com
    username: admin
    password: ${NPM_USWEST_PASSWORD}
    tags: [production, us-west]

  - name: eu-prod
    host: npm-eu.example.com
    username: admin
    password: ${NPM_EU_PASSWORD}
    tags: [production, eu-west]
```

---

## Credential Management

### Environment Variables (Recommended)

Store sensitive passwords in environment variables:

**Linux/macOS:**
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export NPM_PASSWORD="your-secure-password"
export NPM_STAGING_PASSWORD="staging-password"
export NPM_DEV_PASSWORD="dev-password"

# Source the file
source ~/.bashrc
```

**Windows:**
```powershell
# Set user environment variables
[System.Environment]::SetEnvironmentVariable('NPM_PASSWORD', 'your-secure-password', 'User')
```

**Docker:**
```bash
# Pass environment variables to Docker
docker run -i --rm \
  -e NPM_PASSWORD="your-password" \
  -e NPM_STAGING_PASSWORD="staging-password" \
  wadewoolwine/npm-mcp-server:latest
```

**Docker Compose:**
```yaml
services:
  npm-mcp:
    image: wadewoolwine/npm-mcp-server:latest
    environment:
      - NPM_PASSWORD=${NPM_PASSWORD}
      - NPM_STAGING_PASSWORD=${NPM_STAGING_PASSWORD}
    env_file:
      - .env  # Load from .env file
```

### System Keyring (Most Secure)

Use the system keyring for production environments:

**1. Enable keyring support:**

```yaml
instances:
  - name: production
    host: npm.example.com
    username: admin
    use_keyring: true  # Retrieve password from keyring
    keyring_service: npm_mcp  # Optional: custom service name
```

**2. Store password in keyring:**

```bash
# Install keyring support
pip install keyring

# Store password
python -c "import keyring; keyring.set_password('npm_mcp', 'production', 'your-password')"

# Verify storage
python -c "import keyring; print(keyring.get_password('npm_mcp', 'production'))"
```

**3. Update configuration:**

The server will automatically retrieve the password from the keyring using the instance name as the username key.

### Encrypted Configuration File (Alternative)

Encrypt the entire configuration file:

```bash
# Encrypt configuration
openssl enc -aes-256-cbc -salt -in instances.yaml -out instances.yaml.enc

# Decrypt at runtime
openssl enc -aes-256-cbc -d -in instances.yaml.enc -out instances.yaml
```

---

## Global Settings

Global settings control server behavior across all instances.

### Settings Reference

```yaml
settings:
  # Connection settings
  timeout: 30                          # HTTP request timeout (seconds)
  retry_attempts: 3                    # Number of retry attempts for failed requests
  retry_delay: 1.0                     # Initial delay between retries (seconds)
  max_retry_delay: 30.0                # Maximum retry delay (exponential backoff)

  # Authentication settings
  cache_tokens: true                   # Cache JWT tokens to disk
  token_cache_path: ~/.npm-mcp/token_cache  # Token cache directory
  token_refresh_threshold: 300         # Refresh tokens before expiry (seconds)

  # Logging settings
  log_level: INFO                      # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  log_format: json                     # Log format: json or text
  log_file: ~/.npm-mcp/logs/server.log  # Log file path (null for no file logging)
  log_to_stdout: true                  # Log to stdout
  log_http_requests: false             # Log all HTTP requests (verbose)

  # Performance settings
  connection_pool_size: 10             # HTTP connection pool size per instance
  max_concurrent_operations: 50        # Max concurrent operations for bulk operations
  batch_size: 10                       # Default batch size for bulk operations

  # Feature flags
  enable_bulk_operations: true         # Enable bulk operations tool
  enable_audit_log: true               # Enable audit logging
  enable_metrics: false                # Enable metrics collection (future)
```

### Common Settings Configurations

#### Development Environment

```yaml
settings:
  timeout: 60                # Longer timeout for debugging
  retry_attempts: 1          # Minimal retries
  log_level: DEBUG           # Verbose logging
  log_http_requests: true    # Log all HTTP requests
  cache_tokens: false        # Disable token caching
  verify_ssl: false          # Allow self-signed certificates
```

#### Production Environment

```yaml
settings:
  timeout: 30
  retry_attempts: 3
  retry_delay: 2.0
  log_level: INFO            # Standard logging
  log_http_requests: false   # Minimal logging
  cache_tokens: true         # Enable token caching
  token_cache_path: /var/lib/npm-mcp/token_cache
  log_file: /var/log/npm-mcp/server.log
```

#### High-Performance Environment

```yaml
settings:
  timeout: 15                           # Lower timeout
  retry_attempts: 2                     # Fewer retries
  connection_pool_size: 20              # Larger connection pool
  max_concurrent_operations: 100        # Higher concurrency
  batch_size: 25                        # Larger batches
  cache_tokens: true
  log_level: WARNING                    # Minimal logging
```

---

## Environment Variables

### Supported Environment Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `NPM_MCP_CONFIG` | string | Path to configuration file | `/etc/npm-mcp/instances.yaml` |
| `NPM_MCP_LOG_LEVEL` | string | Override log level | `DEBUG`, `INFO`, `WARNING` |
| `NPM_MCP_LOG_FILE` | string | Path to log file | `/var/log/npm-mcp.log` |
| `NPM_MCP_TIMEOUT` | integer | Override timeout (seconds) | `60` |
| `NPM_MCP_CACHE_TOKENS` | boolean | Enable/disable token caching | `true`, `false` |
| `NPM_PASSWORD` | string | Default instance password | `secret-password` |
| `NPM_*_PASSWORD` | string | Instance-specific password | `NPM_PROD_PASSWORD=secret` |

### Variable Interpolation in Configuration

Use `${VARIABLE_NAME}` syntax to reference environment variables:

```yaml
instances:
  - name: production
    host: ${NPM_HOST}                    # From environment
    port: ${NPM_PORT:-81}                # With default value
    username: ${NPM_USERNAME}
    password: ${NPM_PASSWORD}

settings:
  timeout: ${NPM_TIMEOUT:-30}            # Default to 30 if not set
  log_level: ${NPM_LOG_LEVEL:-INFO}
  log_file: ${NPM_LOG_FILE}
```

### .env File Support

Create a `.env` file in the configuration directory:

```bash
# .npm-mcp/.env
NPM_PASSWORD=production-password
NPM_STAGING_PASSWORD=staging-password
NPM_DEV_PASSWORD=dev-password
NPM_TIMEOUT=45
NPM_LOG_LEVEL=DEBUG
```

The server automatically loads `.env` files from:
1. Current working directory
2. Configuration directory (`~/.npm-mcp/`)
3. Parent directories (up to root)

---

## Multi-Instance Setup

Managing multiple NPM instances simultaneously.

### Configuration

```yaml
instances:
  # Production instances
  - name: prod-primary
    host: npm-prod1.example.com
    username: admin
    password: ${NPM_PROD_PRIMARY_PASSWORD}
    default: true
    tags: [production, primary, us-east]

  - name: prod-secondary
    host: npm-prod2.example.com
    username: admin
    password: ${NPM_PROD_SECONDARY_PASSWORD}
    tags: [production, secondary, us-west]

  # Staging instances
  - name: staging-east
    host: npm-staging-east.example.com
    username: admin
    password: ${NPM_STAGING_EAST_PASSWORD}
    tags: [staging, us-east]

  - name: staging-west
    host: npm-staging-west.example.com
    username: admin
    password: ${NPM_STAGING_WEST_PASSWORD}
    tags: [staging, us-west]

  # Development instances
  - name: dev-local
    host: localhost
    port: 81
    use_https: false
    username: admin
    password: ${NPM_DEV_PASSWORD}
    tags: [development, local]
```

### Instance Selection

**Default Instance:**
The instance with `default: true` is used when no instance is specified in operations.

**Selecting Instances:**
- By name: `npm_select_instance(instance_name="staging-east")`
- By tag: Filter instances by tags in list operations
- Context-based: Set instance for session-wide operations

### Instance Management Patterns

#### Environment-Based Configuration

```yaml
# Production
instances:
  - name: prod
    host: npm.example.com
    username: admin
    password: ${NPM_PROD_PASSWORD}
    default: true

---

# Staging (separate file)
instances:
  - name: staging
    host: npm-staging.example.com
    username: admin
    password: ${NPM_STAGING_PASSWORD}
    default: true
```

Load based on environment:
```bash
# Production
export NPM_MCP_CONFIG=~/.npm-mcp/production.yaml

# Staging
export NPM_MCP_CONFIG=~/.npm-mcp/staging.yaml
```

#### Region-Based Configuration

```yaml
instances:
  - name: us-east
    host: npm-useast.example.com
    username: admin
    password: ${NPM_USEAST_PASSWORD}
    tags: [us-east, production]

  - name: us-west
    host: npm-uswest.example.com
    username: admin
    password: ${NPM_USWEST_PASSWORD}
    tags: [us-west, production]

  - name: eu-west
    host: npm-euwest.example.com
    username: admin
    password: ${NPM_EUWEST_PASSWORD}
    tags: [eu-west, production]
```

---

## Security Best Practices

### 1. Credential Security

**DO:**
- ✅ Use environment variables for passwords
- ✅ Use system keyring for production
- ✅ Encrypt configuration files at rest
- ✅ Use strong, unique passwords per instance
- ✅ Rotate credentials regularly
- ✅ Set appropriate file permissions (600 for config files)

**DON'T:**
- ❌ Hard-code passwords in configuration files
- ❌ Commit credentials to version control
- ❌ Share credentials between instances
- ❌ Use default/weak passwords
- ❌ Store credentials in plain text

### 2. File Permissions

```bash
# Set restrictive permissions on configuration
chmod 600 ~/.npm-mcp/instances.yaml

# Set directory permissions
chmod 700 ~/.npm-mcp/

# Verify permissions
ls -la ~/.npm-mcp/
```

### 3. SSL/TLS Configuration

**Production:**
```yaml
instances:
  - name: production
    host: npm.example.com
    use_https: true
    verify_ssl: true  # Always verify in production
```

**Development (Self-Signed Certificates):**
```yaml
instances:
  - name: development
    host: npm-dev.local
    use_https: true
    verify_ssl: false  # Only for development!
    description: "Development only - uses self-signed certificate"
```

### 4. Token Caching Security

**Secure Token Cache:**
```yaml
settings:
  cache_tokens: true
  token_cache_path: ~/.npm-mcp/token_cache  # Secure location
```

**Set Permissions:**
```bash
chmod 700 ~/.npm-mcp/token_cache
```

**Disable in Shared Environments:**
```yaml
settings:
  cache_tokens: false  # Don't cache on shared systems
```

### 5. Audit Logging

**Enable Comprehensive Logging:**
```yaml
settings:
  log_level: INFO
  log_file: /var/log/npm-mcp/server.log
  enable_audit_log: true
  log_http_requests: false  # Only enable for debugging
```

**Secure Log Files:**
```bash
# Create log directory
sudo mkdir -p /var/log/npm-mcp

# Set permissions
sudo chown $USER:$USER /var/log/npm-mcp
chmod 750 /var/log/npm-mcp
```

---

## Advanced Configuration

### Custom Configuration Paths

```bash
# Single config file
export NPM_MCP_CONFIG=/etc/npm-mcp/instances.yaml

# Multiple config files (merged)
export NPM_MCP_CONFIG=/etc/npm-mcp/global.yaml:~/.npm-mcp/personal.yaml
```

### Configuration Validation

Validate configuration before deployment:

```bash
# Validate syntax
npm-mcp --validate-config

# Test connection to all instances
npm-mcp --test-all-instances

# Dry-run mode
npm-mcp --dry-run
```

### Performance Tuning

**High-Throughput Workloads:**
```yaml
settings:
  connection_pool_size: 50
  max_concurrent_operations: 200
  batch_size: 50
  timeout: 15
  retry_attempts: 2
```

**Conservative/Stable Workloads:**
```yaml
settings:
  connection_pool_size: 5
  max_concurrent_operations: 10
  batch_size: 5
  timeout: 60
  retry_attempts: 5
  retry_delay: 3.0
```

### Docker-Specific Configuration

**Docker Compose:**
```yaml
version: '3.8'
services:
  npm-mcp:
    image: wadewoolwine/npm-mcp-server:latest
    volumes:
      - ./config:/config:ro  # Read-only mount
    environment:
      - NPM_MCP_CONFIG=/config/instances.yaml
      - NPM_PASSWORD_FILE=/run/secrets/npm_password  # Docker secrets
    secrets:
      - npm_password
    restart: unless-stopped

secrets:
  npm_password:
    file: ./secrets/npm_password.txt
```

---

## Configuration Examples

### Example 1: Simple Single Instance

```yaml
instances:
  - name: production
    host: npm.example.com
    username: admin
    password: ${NPM_PASSWORD}
    default: true

settings:
  log_level: INFO
  cache_tokens: true
```

### Example 2: Multi-Environment Setup

```yaml
instances:
  - name: production
    host: npm.example.com
    port: 81
    use_https: true
    username: admin
    password: ${NPM_PROD_PASSWORD}
    default: true
    tags: [production, primary]

  - name: staging
    host: npm-staging.example.com
    port: 81
    use_https: true
    username: admin
    password: ${NPM_STAGING_PASSWORD}
    tags: [staging]

  - name: development
    host: localhost
    port: 81
    use_https: false
    username: admin
    password: ${NPM_DEV_PASSWORD}
    tags: [development, local]

settings:
  timeout: 30
  retry_attempts: 3
  log_level: INFO
  cache_tokens: true
  token_cache_path: ~/.npm-mcp/token_cache
```

### Example 3: High-Security Production

```yaml
instances:
  - name: production
    host: npm.example.com
    port: 81
    use_https: true
    verify_ssl: true
    username: admin
    use_keyring: true
    keyring_service: npm_mcp_prod
    default: true

settings:
  timeout: 30
  retry_attempts: 3
  log_level: INFO
  log_file: /var/log/npm-mcp/server.log
  cache_tokens: true
  token_cache_path: /var/lib/npm-mcp/token_cache
  enable_audit_log: true
  log_http_requests: false
```

### Example 4: Development with Debug Logging

```yaml
instances:
  - name: local
    host: localhost
    port: 81
    use_https: false
    username: admin
    password: admin123
    default: true

settings:
  timeout: 60
  retry_attempts: 1
  log_level: DEBUG
  log_http_requests: true
  cache_tokens: false
```

---

## Troubleshooting Configuration Issues

### Issue: Configuration Not Loading

**Check:**
1. File path is correct: `echo $NPM_MCP_CONFIG`
2. File exists: `ls -la ~/.npm-mcp/instances.yaml`
3. YAML syntax is valid: `yamllint instances.yaml`
4. File permissions: `ls -la ~/.npm-mcp/instances.yaml` (should be 600)

### Issue: Environment Variables Not Interpolating

**Check:**
1. Variables are exported: `echo $NPM_PASSWORD`
2. Syntax is correct: `${VARIABLE_NAME}`
3. Variables are accessible to the process
4. No typos in variable names

### Issue: Keyring Authentication Failing

**Check:**
1. Keyring package is installed: `pip list | grep keyring`
2. Password is stored: `python -c "import keyring; print(keyring.get_password('npm_mcp', 'production'))"`
3. Keyring service name matches configuration
4. System keyring is accessible

### Issue: SSL Verification Failures

**Solutions:**
- For self-signed certificates: Set `verify_ssl: false`
- For corporate certificates: Add to system trust store
- For Let's Encrypt: Ensure system certificates are up-to-date

---

## Next Steps

- **Installation**: See [INSTALLATION.md](./INSTALLATION.md)
- **Usage Guide**: See [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- **Tool Reference**: See [TOOL_CATALOG.md](./TOOL_CATALOG.md)
- **Examples**: Check [examples/](../examples/) directory

---

**Last Updated**: 2025-01-28
**Version**: 1.0.0
