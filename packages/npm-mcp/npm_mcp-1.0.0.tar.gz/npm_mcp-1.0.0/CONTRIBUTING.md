# Contributing to NPM MCP Server

Thank you for your interest in contributing to the NPM MCP Server project!

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- A Nginx Proxy Manager instance for testing (optional, can use Docker)

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wadew/npm-mcp.git
   cd npm-mcp
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation**:
   ```bash
   python -m npm_mcp
   pytest --version
   ruff --version
   mypy --version
   ```

### Development Workflow

This project follows **strict Test-Driven Development (TDD)**. Please read `.claude/CLAUDE.md` for complete development guidelines.

#### TDD Cycle

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make it pass
3. **REFACTOR**: Improve code quality while keeping tests green

Example:
```bash
# 1. Write test
vim tests/unit/test_config/test_loader.py

# 2. Run test (should fail)
pytest tests/unit/test_config/test_loader.py -v

# 3. Implement feature
vim src/npm_mcp/config/loader.py

# 4. Run test again (should pass)
pytest tests/unit/test_config/test_loader.py -v

# 5. Refactor if needed
# 6. Run full test suite
pytest
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/unit/test_config/test_loader.py

# Run specific test
pytest tests/unit/test_config/test_loader.py::test_load_yaml_config

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Code Quality Checks

Before committing, ensure all quality checks pass:

```bash
# Run linter
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Run type checker
mypy src/

# Run all checks
ruff check . && mypy src/ && pytest
```

### Code Coverage Requirements

- **Overall**: Minimum 80% coverage
- **Critical modules** (auth, client): Minimum 85% coverage
- All new code must include tests

Check coverage:
```bash
pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

### Project Structure

```
npm-mcp/
├── .claude/                  # Claude Code project management
│   └── CLAUDE.md             # Development guidelines (READ THIS!)
├── src/npm_mcp/              # Source code
│   ├── config/               # Configuration management
│   ├── auth/                 # Authentication
│   ├── client/               # HTTP client
│   ├── models/               # Data models
│   ├── tools/                # MCP tools
│   └── utils/                # Utilities
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── docs/                     # Documentation
└── examples/                 # Example scripts
```

### Commit Guidelines

Use conventional commit format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

**Example**:
```bash
git commit -m "feat: implement JWT token caching with encryption

- Add TokenCache class with memory and disk storage
- Implement encryption using cryptography.fernet
- Add tests for cache operations and expiration
- Coverage: 92%

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes following TDD
3. Ensure all tests pass and coverage is maintained
4. Ensure all linters pass
5. Update documentation if needed
6. Commit with conventional commit message
7. Push to origin:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create pull request on GitHub
9. Wait for CI checks to pass
10. Request review

### Pull Request Requirements

- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] All linters passing (ruff, mypy)
- [ ] Documentation updated
- [ ] Conventional commit format
- [ ] At least one approval

### Getting Help

- **Documentation**: Check `docs/` directory
- **Guidelines**: Read `.claude/CLAUDE.md` thoroughly
- **Issues**: [GitHub Issues](https://github.com/wadew/npm-mcp/issues) for bug reports
- **Questions**: [GitHub Discussions](https://github.com/wadew/npm-mcp/discussions)

### Local NPM Instance for Testing

To set up a local NPM instance for testing:

```bash
# Using Docker
docker run -d \
  --name npm-test \
  -p 80:80 \
  -p 81:81 \
  -p 443:443 \
  jc21/nginx-proxy-manager:latest

# Access NPM admin at http://localhost:81
# Default credentials: admin@example.com / changeme
```

Create a test configuration:
```bash
cp docs/instances.example.yaml instances.yaml
# Edit instances.yaml with your local NPM details
```

### Useful Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run MCP server
python -m npm_mcp

# Run specific test with verbose output
pytest tests/unit/test_config/test_loader.py -vv

# Run tests with stdout
pytest -s

# Run tests in parallel (faster)
pytest -n auto

# Watch mode (re-run on file changes)
ptw  # Requires pytest-watch: pip install pytest-watch

# Generate test coverage report
pytest --cov --cov-report=html
```

### Resources

- **PRD**: `docs/PRD.md` - Complete product requirements
- **Tool Catalog**: `docs/TOOL_CATALOG.md` - All MCP tools
- **CLAUDE.md**: `.claude/CLAUDE.md` - Development guidelines
- **MCP Docs**: https://modelcontextprotocol.io/
- **Python MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **NPM API**: Check your NPM instance at `/api/schema`

## Code of Conduct

- Be respectful and professional
- Follow TDD methodology strictly
- Write tests for all code
- Document your code thoroughly
- Ask questions when unclear
- Help others learn and grow

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Happy coding!** If you have questions, don't hesitate to ask.
