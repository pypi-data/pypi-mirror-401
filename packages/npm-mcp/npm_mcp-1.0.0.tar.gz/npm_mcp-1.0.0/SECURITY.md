# Security Policy

## Supported Versions

The following versions of npm-mcp are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in npm-mcp, please report it through GitHub's Security Advisories feature.

### How to Report

1. Go to the [Security Advisories](https://github.com/wadew/npm-mcp/security/advisories) page
2. Click "Report a vulnerability"
3. Fill out the advisory form with:
   - A clear description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Any suggested fixes (optional)

### What to Expect

- **Initial Response**: Within 48 hours of your report, you will receive an acknowledgment
- **Assessment**: Within 7 days, we will assess the vulnerability and provide a severity rating
- **Resolution**: Critical and high-severity issues will be prioritized for immediate patching
- **Disclosure**: We follow coordinated disclosure practices and will work with you on timing

### Security Best Practices

When using npm-mcp, please follow these security guidelines:

1. **Credentials Management**
   - Never hardcode NPM credentials in configuration files
   - Use environment variables with the `${VAR}` syntax
   - Consider using the keyring integration for secure credential storage

2. **Network Security**
   - Always use HTTPS (`use_https: true`) when connecting to NPM instances
   - Verify SSL certificates in production environments
   - Use firewall rules to restrict access to NPM management ports

3. **Access Control**
   - Create dedicated NPM users for the MCP server with minimal required permissions
   - Regularly rotate credentials
   - Review and audit access lists periodically

4. **Configuration**
   - Keep the `instances.yaml` configuration file secure (mode 600)
   - Never commit configuration files with credentials to version control
   - Use the encryption features for sensitive data at rest

## Security Features

npm-mcp includes several security features:

- **Encrypted Token Cache**: JWT tokens can be cached with Fernet encryption
- **Credential Masking**: Sensitive data is automatically redacted from logs
- **Secure Defaults**: HTTPS is recommended, credentials are validated before storage
- **Minimal Permissions**: The server operates with least-privilege principles

## Acknowledgments

We appreciate security researchers who help keep npm-mcp safe. Contributors who report valid vulnerabilities will be acknowledged (with permission) in our release notes.
