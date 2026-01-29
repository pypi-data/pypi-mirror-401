# Nginx Proxy Manager MCP Server

A comprehensive Model Context Protocol (MCP) server that enables Large Language Models to manage Nginx Proxy Manager instances through natural language interactions.

## Overview

This MCP server provides full-featured access to Nginx Proxy Manager's API, allowing AI assistants like Claude to:

- Configure reverse proxy hosts with SSL termination
- Manage SSL certificates (Let's Encrypt and custom)
- Control access lists and authentication
- Set up TCP/UDP stream forwarding
- Manage URL redirections and dead hosts
- Administer users and system settings
- Handle multiple NPM instances simultaneously

## Key Features

### Full NPM API Coverage
- **100% API coverage**: All NPM endpoints supported
- **28 semantic tools**: Intelligently grouped operations with full instance CRUD (not 1:1 API mapping)
- **Pydantic validation**: Type-safe operations with automatic validation
- **Structured outputs**: JSON schema-validated responses

### Multi-Instance Management
- **Unlimited instances**: Manage production, staging, homelab, and more
- **Instance contexts**: Switch between instances seamlessly
- **Credential security**: Encrypted storage with multiple options
- **Cross-instance sync**: Replicate configurations across instances

### Production-Ready
- **JWT authentication**: Secure token management with auto-refresh
- **Retry logic**: Exponential backoff for failed requests
- **Connection pooling**: Efficient HTTP connection reuse
- **Comprehensive logging**: Structured logs with audit trail
- **Error handling**: Graceful degradation with actionable error messages

### MCP Best Practices (2025)
- **Semantic grouping**: Higher-level tools instead of raw API exposure
- **Schema validation**: Automatic input/output validation
- **Clear documentation**: Comprehensive tool descriptions and examples
- **Async operations**: Non-blocking I/O for performance
- **Containerization**: Docker support for consistent deployment

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/npm-mcp.git
cd npm-mcp

# Install dependencies
pip install -e .

# Or using Poetry
poetry install
```

### Configuration

1. Create a configuration file:

```bash
mkdir -p ~/.npm-mcp
cp docs/instances.example.yaml ~/.npm-mcp/instances.yaml
```

2. Edit the configuration with your NPM instances:

```yaml
instances:
  - name: "production"
    host: "npm.example.com"
    port: 81
    use_https: true
    username: "admin@example.com"
    password: "${NPM_PROD_PASSWORD}"
    default: true
```

3. Set environment variables:

```bash
export NPM_PROD_PASSWORD="your_secure_password"
```

### Running the MCP Server

```bash
# Start the MCP server
npm-mcp

# Or with custom config
NPM_MCP_CONFIG=/path/to/config.yaml npm-mcp

# Docker
docker run -v ~/.npm-mcp:/config npm-mcp
```

### Using with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "nginx-proxy-manager": {
      "command": "npm-mcp",
      "env": {
        "NPM_MCP_CONFIG": "/Users/youruser/.npm-mcp/instances.yaml",
        "NPM_PROD_PASSWORD": "your_password"
      }
    }
  }
}
```

## Usage Examples

### Creating a Proxy Host

> "Create a proxy host for api.example.com pointing to 192.168.1.100:3000 with SSL certificate ID 5 and force HTTPS"

```json
{
  "tool": "npm_manage_proxy_host",
  "arguments": {
    "operation": "create",
    "domain_names": ["api.example.com"],
    "forward_host": "192.168.1.100",
    "forward_port": 3000,
    "forward_scheme": "http",
    "certificate_id": 5,
    "force_ssl": true,
    "http2_support": true,
    "websocket_support": true,
    "block_exploits": true
  }
}
```

### Managing SSL Certificates

> "Create a Let's Encrypt wildcard certificate for *.example.com using Cloudflare DNS challenge"

```json
{
  "tool": "npm_manage_certificate",
  "arguments": {
    "operation": "create",
    "provider": "letsencrypt",
    "nice_name": "Example Wildcard Certificate",
    "domain_names": ["*.example.com", "example.com"],
    "letsencrypt_email": "admin@example.com",
    "letsencrypt_agree_tos": true,
    "dns_challenge": true,
    "dns_provider": "cloudflare",
    "dns_credentials": "{\"api_token\":\"your_cloudflare_token\"}"
  }
}
```

### Bulk Operations

> "Renew all certificates expiring in the next 30 days"

```json
{
  "tool": "npm_bulk_update_certificates",
  "arguments": {
    "operation": "renew",
    "renew_expiring": true,
    "days_threshold": 30
  }
}
```

### Multi-Instance Management

> "Sync proxy hosts from production to staging"

```json
{
  "tool": "npm_sync_configuration",
  "arguments": {
    "source_instance": "production",
    "target_instance": "staging",
    "resources": ["proxy_hosts", "certificates"],
    "mode": "mirror",
    "dry_run": true
  }
}
```

## Documentation

### Core Documents

- **[Product Requirements Document (PRD)](./PRD.md)**: Complete project requirements, architecture, and implementation plan
- **[Tool Catalog](./TOOL_CATALOG.md)**: Comprehensive guide to all 25 MCP tools with examples
- **[Configuration Guide](./instances.example.yaml)**: Detailed configuration file with all options

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         LLM Client                           │
│                    (Claude, ChatGPT, etc.)                   │
└──────────────────────────────┬──────────────────────────────┘
                               │ MCP Protocol
┌──────────────────────────────▼──────────────────────────────┐
│                    MCP Server (Python)                       │
├──────────────────────────────────────────────────────────────┤
│  • Tool Registry & Router (28 semantic tools)                │
│  • Instance Configuration Manager                            │
│  • Authentication & Session Manager (JWT)                    │
│  • NPM API Client (httpx + retry logic)                      │
│  • Validation & Schema Layer (Pydantic)                      │
│  • Logging & Audit System                                    │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP/REST
┌──────────────────────────────▼──────────────────────────────┐
│              NPM Instance(s) API (Port 81)                   │
└──────────────────────────────────────────────────────────────┘
```

## Tool Categories

The MCP server provides **28 semantic tools** organized into 9 categories:

1. **Instance Management** (7 tools): Full CRUD operations on NPM instance configurations with persistent storage
2. **Proxy Host Management** (3 tools): Create and manage reverse proxy hosts
3. **Certificate Management** (3 tools): Handle SSL/TLS certificates
4. **Access Control** (2 tools): Manage IP-based access lists and HTTP auth
5. **Stream Management** (2 tools): Configure TCP/UDP stream forwarding
6. **Redirection & Dead Hosts** (2 tools): Set up URL redirects and 404 handlers
7. **User Management** (2 tools): Administer NPM users and permissions
8. **System & Reporting** (4 tools): System settings, audit logs, and reports
9. **Bulk Operations** (3 tools): Batch operations for efficiency

See [Tool Catalog](./TOOL_CATALOG.md) for detailed documentation.

## Security

### Authentication
- JWT token-based authentication
- Automatic token refresh with expiration handling
- Support for pre-generated API tokens

### Credential Storage
Multiple secure options:
1. **Environment variables** (recommended for production)
2. **Encrypted configuration file**
3. **System keyring** (macOS Keychain, Windows Credential Manager)
4. **Secrets manager integration** (AWS, Vault - future)

### Best Practices
- Never commit credentials to version control
- Use HTTPS for NPM connections when possible
- Implement proper file permissions (`chmod 600` for config files)
- Enable audit logging for compliance
- Regular credential rotation

## Development

### Project Structure

```
npm-mcp/
├── pyproject.toml              # Project metadata
├── README.md                   # This file
├── docs/                       # Documentation
│   ├── PRD.md                  # Product requirements
│   ├── TOOL_CATALOG.md         # Tool reference
│   └── instances.example.yaml  # Config example
├── src/npm_mcp/                # Source code
│   ├── server.py               # MCP server
│   ├── config/                 # Configuration
│   ├── auth/                   # Authentication
│   ├── client/                 # NPM API client
│   ├── models/                 # Pydantic models
│   ├── tools/                  # MCP tools
│   └── utils/                  # Utilities
└── tests/                      # Test suite
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# With coverage
pytest --cov=npm_mcp --cov-report=html

# Run specific test
pytest tests/test_tools/test_proxy_host.py
```

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/npm-mcp.git
cd npm-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run linters
ruff check .
mypy src/

# Format code
ruff format .
```

## Dependencies

### Core
- **Python**: >= 3.11
- **mcp**: >= 1.19.0 (Official MCP SDK)
- **httpx**: >= 0.28.0 (Async HTTP client)
- **pydantic**: >= 2.12.0 (Data validation)
- **pyyaml**: >= 6.0.3 (Config parsing)
- **cryptography**: >= 46.0.0 (Encryption)
- **keyring**: >= 25.6.0 (OS credential storage)
- **python-dotenv**: >= 1.1.0 (Environment variables)
- **structlog**: >= 25.4.0 (Structured logging)
- **tenacity**: >= 9.1.0 (Retry logic)

### Development
- **pytest**: >= 8.4.0 (Testing framework)
- **pytest-asyncio**: >= 1.2.0 (Async testing)
- **pytest-cov**: >= 7.0.0 (Coverage reporting)
- **pytest-mock**: >= 3.15.0 (Mocking)
- **ruff**: >= 0.14.0 (Linting and formatting)
- **mypy**: >= 1.18.0 (Type checking)
- **types-pyyaml**: >= 6.0.12 (Type stubs)

See [pyproject.toml](../pyproject.toml) for complete dependency list.

## Roadmap

### Phase 1: Foundation (Weeks 1-2) ✓
- Configuration system
- Authentication and token management
- HTTP client with retry logic
- Pydantic models

### Phase 2: Core Tools (Weeks 3-4)
- MCP server setup
- Instance, proxy host, certificate, and access list tools
- Unit tests

### Phase 3: Extended Features (Weeks 5-6)
- Stream, redirection, user, and system tools
- Integration tests

### Phase 4: Advanced Features (Weeks 7-8)
- Bulk operations
- Cross-instance sync
- Performance optimization

### Phase 5: Release (Weeks 9-10)
- Documentation completion
- Docker containerization
- CI/CD pipeline
- PyPI release

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Support

- **Documentation**: See [docs/](./docs/) directory
- **Issues**: [GitHub Issues](https://github.com/yourusername/npm-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/npm-mcp/discussions)

## License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) file for details.

## Acknowledgments

- [Nginx Proxy Manager](https://nginxproxymanager.com/) - The excellent reverse proxy manager
- [Anthropic MCP](https://modelcontextprotocol.io/) - The Model Context Protocol
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Official Python implementation

## Related Projects

- [Nginx Proxy Manager](https://github.com/NginxProxyManager/nginx-proxy-manager)
- [MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Claude Desktop](https://claude.ai/download)

---

**Status**: Documentation Complete - Ready for Implementation

**Last Updated**: 2025-10-26

**Version**: 1.0.0
