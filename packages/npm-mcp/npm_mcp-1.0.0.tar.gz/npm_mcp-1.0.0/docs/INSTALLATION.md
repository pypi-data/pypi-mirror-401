# Installation Guide

This guide provides comprehensive installation instructions for the NPM MCP Server across different platforms and deployment scenarios.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
  - [Option 1: Install via pip](#option-1-install-via-pip-recommended)
  - [Option 2: Docker](#option-2-docker)
  - [Option 3: From Source](#option-3-from-source)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Configuration Setup](#configuration-setup)
- [Verification](#verification)
- [Upgrading](#upgrading)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Linux, macOS, Windows (with WSL2 for Docker) |
| Python | >= 3.11 (3.11, 3.12, or 3.13 supported) |
| RAM | 512MB minimum, 1GB recommended |
| Disk Space | 500MB for installation and dependencies |
| Network | HTTPS access to NPM instances (typically port 81) |

### Recommended Setup

- **Python**: 3.11 or 3.13 (most tested versions)
- **Package Manager**: `uv` (faster) or `pip` (standard)
- **Shell**: bash, zsh, or compatible
- **Claude Desktop**: Latest version (for MCP integration)

## Installation Methods

### Option 1: Install via pip (Recommended)

This is the simplest and most common installation method.

#### 1.1 Install from PyPI

```bash
# Install the latest stable version
pip install npm-mcp-server

# Or with a specific version
pip install npm-mcp-server==1.0.0
```

#### 1.2 Verify Installation

```bash
# Check installation
npm-mcp --version

# Or
python -m npm_mcp --version
```

#### 1.3 Install in Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv npm-mcp-env

# Activate it (Linux/macOS)
source npm-mcp-env/bin/activate

# Activate it (Windows)
npm-mcp-env\Scripts\activate

# Install the package
pip install npm-mcp-server

# Verify
npm-mcp --version
```

#### 1.4 Install with uv (Faster Alternative)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a project with uv
uv init npm-mcp-project
cd npm-mcp-project

# Add npm-mcp-server as a dependency
uv add npm-mcp-server

# Run the server
uv run npm-mcp
```

---

### Option 2: Docker

Docker provides a consistent, isolated environment for running the NPM MCP Server.

#### 2.1 Prerequisites

- Docker Engine 20.10+ or Docker Desktop
- Docker Compose (optional, for multi-container setups)

#### 2.2 Pull from Docker Hub

```bash
# Pull the latest version
docker pull wadewoolwine/npm-mcp-server:latest

# Or pull a specific version
docker pull wadewoolwine/npm-mcp-server:1.0.0
```

#### 2.3 Run with Docker

```bash
# Basic run (stdio mode for MCP)
docker run -i --rm wadewoolwine/npm-mcp-server:latest

# Run with configuration volume
docker run -i --rm \
  -v ~/.npm-mcp:/config \
  -e NPM_MCP_CONFIG=/config/instances.yaml \
  wadewoolwine/npm-mcp-server:latest

# Run with environment variables
docker run -i --rm \
  -v ~/.npm-mcp:/config \
  -e NPM_MCP_CONFIG=/config/instances.yaml \
  -e NPM_PASSWORD="your-password" \
  -e NPM_STAGING_PASSWORD="staging-password" \
  wadewoolwine/npm-mcp-server:latest
```

#### 2.4 Docker Compose Setup

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  npm-mcp-server:
    image: wadewoolwine/npm-mcp-server:latest
    stdin_open: true
    tty: true
    volumes:
      - ~/.npm-mcp:/config
    environment:
      - NPM_MCP_CONFIG=/config/instances.yaml
      - NPM_PASSWORD=${NPM_PASSWORD}
      - NPM_STAGING_PASSWORD=${NPM_STAGING_PASSWORD}
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

#### 2.5 Build from Source

If you want to build the Docker image yourself:

```bash
# Clone the repository
git clone https://github.com/wadew/npm-mcp.git
cd npm-mcp

# Build the image
docker build -t npm-mcp-server:local .

# Check image size (should be < 200MB)
docker images npm-mcp-server:local --format "{{.Size}}"

# Run your local build
docker run -i --rm npm-mcp-server:local
```

---

### Option 3: From Source

Install directly from the GitHub repository for development or customization.

#### 3.1 Prerequisites

- Git
- Python >= 3.11
- `uv` or `pip`

#### 3.2 Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/wadew/npm-mcp.git
cd npm-mcp

# Or clone via SSH
git clone git@github.com:wadew/npm-mcp.git
cd npm-mcp
```

#### 3.3 Install with uv (Recommended for Development)

```bash
# Install uv if not installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates .venv automatically)
uv sync

# Run the server
uv run python -m npm_mcp

# Or activate the virtual environment
source .venv/bin/activate
python -m npm_mcp
```

#### 3.4 Install with pip

```bash
# Create virtual environment
python -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Run the server
python -m npm_mcp
```

#### 3.5 Verify Source Installation

```bash
# Run tests to ensure everything works
pytest

# Check coverage
pytest --cov=src/npm_mcp --cov-report=term

# Run linters
ruff check .
mypy src/
```

---

## Claude Desktop Integration

The NPM MCP Server integrates with Claude Desktop to provide natural language NPM management.

### Configuration Locations

| Platform | Configuration Path |
|----------|-------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Linux | `~/.config/claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

### Integration Methods

#### Method 1: Using pip Installation

If you installed via pip, use the `npm-mcp` command:

```json
{
  "mcpServers": {
    "npm-mcp": {
      "command": "npm-mcp"
    }
  }
}
```

**With Virtual Environment:**

```json
{
  "mcpServers": {
    "npm-mcp": {
      "command": "/path/to/npm-mcp-env/bin/npm-mcp"
    }
  }
}
```

#### Method 2: Using uv

If you're using uv for development:

```json
{
  "mcpServers": {
    "npm-mcp": {
      "command": "uv",
      "args": ["run", "npm-mcp"],
      "cwd": "/path/to/npm_mcp"
    }
  }
}
```

#### Method 3: Using Docker

For Docker-based deployment:

```json
{
  "mcpServers": {
    "npm-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "${HOME}/.npm-mcp:/config",
        "-e",
        "NPM_MCP_CONFIG=/config/instances.yaml",
        "-e",
        "NPM_PASSWORD",
        "-e",
        "NPM_STAGING_PASSWORD",
        "wadewoolwine/npm-mcp-server:latest"
      ]
    }
  }
}
```

#### Method 4: Using Python Module Directly

For source installations:

```json
{
  "mcpServers": {
    "npm-mcp": {
      "command": "/path/to/.venv/bin/python",
      "args": ["-m", "npm_mcp"],
      "cwd": "/path/to/npm_mcp"
    }
  }
}
```

### Applying Claude Desktop Configuration

1. Edit the appropriate `claude_desktop_config.json` file
2. Add the `npm-mcp` server configuration
3. Save the file
4. Restart Claude Desktop completely (Quit and reopen)
5. Verify the MCP server appears in Claude's available tools

### Troubleshooting Claude Desktop Integration

**Server Not Appearing:**
- Check the configuration file syntax (valid JSON)
- Verify the command path is correct
- Check Claude Desktop logs: `~/Library/Logs/Claude/` (macOS)

**Permission Errors:**
- Ensure the command is executable: `chmod +x /path/to/npm-mcp`
- Verify Docker permissions if using Docker

**Configuration Not Loading:**
- Restart Claude Desktop completely
- Check for syntax errors in JSON
- Verify environment variables are accessible

---

## Configuration Setup

### 1. Create Configuration Directory

```bash
mkdir -p ~/.npm-mcp
```

### 2. Create Instance Configuration

Create `~/.npm-mcp/instances.yaml`:

```yaml
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

settings:
  timeout: 30
  retry_attempts: 3
  retry_delay: 1.0
  log_level: INFO
  cache_tokens: true
  token_cache_path: ~/.npm-mcp/token_cache
```

### 3. Set Environment Variables

**Linux/macOS:**

```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export NPM_PASSWORD="your-production-password"
export NPM_STAGING_PASSWORD="your-staging-password"

# Or create a .env file
echo 'NPM_PASSWORD=your-production-password' >> ~/.npm-mcp/.env
echo 'NPM_STAGING_PASSWORD=your-staging-password' >> ~/.npm-mcp/.env
```

**Windows:**

```powershell
# Set environment variables
[System.Environment]::SetEnvironmentVariable('NPM_PASSWORD', 'your-production-password', 'User')
[System.Environment]::SetEnvironmentVariable('NPM_STAGING_PASSWORD', 'your-staging-password', 'User')
```

### 4. Secure Credentials (Recommended)

For production environments, use the keyring for credential storage:

```bash
# Install keyring support
pip install keyring

# Store credentials securely
python -c "import keyring; keyring.set_password('npm_mcp', 'production', 'your-password')"
```

Update `instances.yaml` to use keyring:

```yaml
instances:
  - name: production
    host: npm.example.com
    port: 81
    use_https: true
    username: admin
    use_keyring: true  # Use system keyring instead of password
```

For detailed configuration options, see [CONFIGURATION.md](./CONFIGURATION.md).

---

## Verification

### Verify Installation

```bash
# Check version
npm-mcp --version

# Or with Python
python -m npm_mcp --version
```

### Verify Configuration

```bash
# Test configuration (dry-run mode)
npm-mcp --test-config

# List configured instances
npm-mcp --list-instances
```

### Verify MCP Tools

Run the server and check available tools (requires Claude Desktop or MCP inspector):

```bash
# Run server in stdio mode
npm-mcp

# In another terminal, use MCP inspector
npx @modelcontextprotocol/inspector npm-mcp
```

### Verify NPM Connectivity

Test connection to your NPM instance:

```bash
# Test connection
npm-mcp --test-connection production
```

---

## Upgrading

### Upgrade via pip

```bash
# Upgrade to latest version
pip install --upgrade npm-mcp-server

# Upgrade to specific version
pip install --upgrade npm-mcp-server==1.0.1
```

### Upgrade via Docker

```bash
# Pull latest image
docker pull wadewoolwine/npm-mcp-server:latest

# Remove old containers (if running)
docker ps -a | grep npm-mcp-server | awk '{print $1}' | xargs docker rm -f

# Restart with new image
docker run -i --rm \
  -v ~/.npm-mcp:/config \
  -e NPM_MCP_CONFIG=/config/instances.yaml \
  wadewoolwine/npm-mcp-server:latest
```

### Upgrade from Source

```bash
cd npm_mcp

# Pull latest changes
git pull origin main

# Update dependencies
uv sync

# Or with pip
pip install -e ".[dev]" --upgrade
```

### Migration Notes

**0.x → 1.0:**
- Configuration format is backward compatible
- No breaking changes in instance configuration
- Bulk operations now use unified tool (update scripts if needed)
- Review [CHANGELOG.md](../CHANGELOG.md) for details

---

## Troubleshooting

### Common Issues

#### Issue: `npm-mcp: command not found`

**Solution:**
- Ensure the package is installed: `pip list | grep npm-mcp`
- Check PATH includes Python scripts directory:
  - Linux/macOS: `~/.local/bin` or `venv/bin`
  - Windows: `%APPDATA%\Python\Python311\Scripts`
- Use full path or activate virtual environment

#### Issue: `ModuleNotFoundError: No module named 'npm_mcp'`

**Solution:**
- Virtual environment not activated
- Wrong Python interpreter
- Package not installed in current environment

```bash
# Check current interpreter
which python

# Activate correct environment
source /path/to/.venv/bin/activate

# Reinstall if needed
pip install npm-mcp-server
```

#### Issue: Docker Permission Denied

**Solution:**
- Add user to docker group (Linux):
  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```
- Use Docker Desktop (macOS/Windows)
- Run with sudo (not recommended for production)

#### Issue: Claude Desktop Not Loading Server

**Solution:**
- Check JSON syntax in config file
- Verify command path exists and is executable
- Check Claude Desktop logs
- Restart Claude Desktop completely
- Verify environment variables are set

#### Issue: Connection Refused to NPM Instance

**Solution:**
- Verify NPM instance is accessible: `curl https://npm.example.com:81/api/`
- Check firewall rules
- Verify credentials in configuration
- Check NPM instance is running
- Test with NPM web UI first

#### Issue: SSL Certificate Verification Failed

**Solution:**
- For self-signed certificates, add to configuration:
  ```yaml
  instances:
    - name: production
      host: npm.example.com
      verify_ssl: false  # For self-signed certs only
  ```
- Or add certificate to system trust store

---

## Platform-Specific Notes

### macOS

```bash
# Install Python if needed
brew install python@3.11

# Install npm-mcp
pip3 install npm-mcp-server

# Configuration location
~/.npm-mcp/instances.yaml

# Claude Desktop config
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux (Ubuntu/Debian)

```bash
# Install Python if needed
sudo apt update
sudo apt install python3.11 python3-pip

# Install npm-mcp
pip3 install npm-mcp-server

# Configuration location
~/.npm-mcp/instances.yaml

# Claude Desktop config (if using)
~/.config/claude/claude_desktop_config.json
```

### Windows

```powershell
# Install Python from python.org or Microsoft Store

# Install npm-mcp
pip install npm-mcp-server

# Configuration location
%USERPROFILE%\.npm-mcp\instances.yaml

# Claude Desktop config
%APPDATA%\Claude\claude_desktop_config.json
```

### Docker (All Platforms)

Docker provides consistent behavior across all platforms:

```bash
# Same commands work on macOS, Linux, and Windows with WSL2
docker pull wadewoolwine/npm-mcp-server:latest
docker run -i --rm \
  -v ~/.npm-mcp:/config \
  -e NPM_MCP_CONFIG=/config/instances.yaml \
  wadewoolwine/npm-mcp-server:latest
```

---

## Next Steps

After installation:

1. **Configure Instances**: See [CONFIGURATION.md](./CONFIGURATION.md)
2. **Learn Usage**: See [USAGE_GUIDE.md](./USAGE_GUIDE.md)
3. **Explore Tools**: See [TOOL_CATALOG.md](./TOOL_CATALOG.md)
4. **Review Examples**: Check [examples/](../examples/) directory

## Support

- **Documentation**: [docs/](../)
- **Issues**: [GitHub Issues](https://github.com/wadew/npm-mcp/issues)
- **Changelog**: [CHANGELOG.md](../CHANGELOG.md)

---

**Last Updated**: 2025-01-28
**Version**: 1.0.0
