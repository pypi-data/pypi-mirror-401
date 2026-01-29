# Troubleshooting Guide

Common issues and solutions for npm-mcp.

## Connection Issues

### "Connection refused" or "Cannot connect to host"

**Symptoms:** Tools fail with connection errors.

**Solutions:**
1. Verify NPM is running and accessible:
   ```bash
   curl -k https://your-npm-host:81/api/
   ```
2. Check firewall rules allow access to port 81 (or your configured port)
3. Verify `host` and `port` in your configuration
4. If using Docker, ensure the container can reach the NPM network

### "SSL certificate verify failed"

**Symptoms:** HTTPS connections fail with certificate errors.

**Solutions:**
1. If using self-signed certificates, set `verify_ssl: false` in config (not recommended for production)
2. Add your CA certificate to the system trust store
3. Ensure the certificate hostname matches your configured host

### "401 Unauthorized" or "Invalid credentials"

**Symptoms:** Authentication fails despite correct credentials.

**Solutions:**
1. Verify username is the email address used for NPM login
2. Check password is correct (try logging into NPM web UI)
3. Ensure the user account is not disabled
4. Clear cached tokens: delete `~/.config/npm-mcp/tokens/`

## Configuration Issues

### "No instances configured"

**Symptoms:** Tools fail saying no instance is available.

**Solutions:**
1. Create configuration file at `~/.config/npm-mcp/instances.yaml`
2. Or set environment variables: `NPM_HOST`, `NPM_USERNAME`, `NPM_PASSWORD`
3. Verify YAML syntax is correct

### Environment variables not working

**Symptoms:** `${VAR}` references not being replaced.

**Solutions:**
1. Ensure variables are exported: `export NPM_PASSWORD="value"`
2. Check variable names match exactly (case-sensitive)
3. Restart the MCP server after setting variables

### Configuration file not found

**Symptoms:** Server starts but can't find config.

**Solutions:**
Check these locations (in order of precedence):
1. `./instances.yaml` (current directory)
2. `~/.config/npm-mcp/instances.yaml`
3. `/etc/npm-mcp/instances.yaml`

## Tool-Specific Issues

### Certificate creation fails

**Symptoms:** Let's Encrypt certificate requests fail.

**Solutions:**
1. Verify domain DNS points to your server
2. Ensure port 80 is accessible for HTTP challenge
3. Check Let's Encrypt rate limits (5 failures per hour per domain)
4. For wildcards, DNS challenge is required with proper provider credentials

### Proxy host creation fails with "domain already exists"

**Symptoms:** Cannot create proxy host for a domain.

**Solutions:**
1. Check if domain exists: ask to "list proxy hosts for domain.com"
2. Update existing host instead of creating new
3. Delete existing host first if replacement is intended

### Bulk operations timeout

**Symptoms:** Large bulk operations fail or hang.

**Solutions:**
1. Reduce `batch_size` parameter (default: 10)
2. Use `dry_run: true` first to preview changes
3. Break into smaller batches manually

## Debugging

### Enable Debug Logging

Set environment variable:
```bash
export NPM_MCP_LOG_LEVEL=DEBUG
npm-mcp
```

Or in Claude Desktop config:
```json
{
  "mcpServers": {
    "npm": {
      "command": "npm-mcp",
      "env": {
        "NPM_MCP_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### View Raw API Responses

Enable HTTP debug logging:
```bash
export HTTPX_LOG_LEVEL=DEBUG
```

### Check Token Cache

Tokens are cached at `~/.config/npm-mcp/tokens/`. To force re-authentication:
```bash
rm -rf ~/.config/npm-mcp/tokens/
```

## Getting Help

If you're still stuck:

1. Check [GitHub Issues](https://github.com/wadew/npm-mcp/issues) for similar problems
2. Open a new issue with:
   - npm-mcp version (`pip show npm-mcp`)
   - Python version (`python --version`)
   - NPM version
   - Debug logs (with credentials redacted)
   - Steps to reproduce
