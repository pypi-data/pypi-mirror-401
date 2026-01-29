# GitLab CI/CD Quick Reference

## Quick Commands

### Run Locally Before Push
```bash
# Install dependencies
uv sync --all-extras

# Run all checks (recommended before every commit)
uv run pytest --cov=src/npm_mcp --cov-report=term-missing && \
uv tool run ruff check --fix . && \
uv tool run ruff format . && \
uv run mypy src/

# Just tests
uv run pytest

# Just linting
uv tool run ruff check .

# Just formatting
uv tool run ruff format .

# Just type checking
uv run mypy src/
```

### Fix Common Issues
```bash
# Fix linting violations automatically
uv tool run ruff check --fix .

# Format all code
uv tool run ruff format .

# Update dependencies
uv lock --upgrade

# Clear local cache
rm -rf .cache/ .venv/
uv sync --all-extras
```

## Pipeline Job Summary

### Must Pass (Block Merge)
- ✅ `test:py3.11` - Primary Python tests, 80%+ coverage required
- ✅ `lint:ruff` - Code style and linting
- ✅ `security:credentials` - No hardcoded secrets

### Can Fail (Warnings Only)
- ⚠️ `test:py3.12` - Python 3.12 compatibility
- ⚠️ `test:py3.13` - Python 3.13 compatibility
- ⚠️ `lint:mypy` - Type checking (informational)
- ⚠️ `security:pip-audit` - Low-severity vulnerabilities
- ⚠️ `security:bandit` - Low-severity security issues

### GitLab-Managed Scanners
- 🔒 `semgrep-sast` - Application security testing
- 🔒 `secret_detection` - Secret scanning
- 🔒 `gemnasium-python-dependency_scanning` - Dependency vulnerabilities

## Reading Test Results

### Coverage Report
```
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
src/npm_mcp/__init__.py                 12      0   100%
src/npm_mcp/server.py                  156     24    85%   45-48, 112-115
src/npm_mcp/auth/manager.py            234     19    92%   156, 178-192
------------------------------------------------------------------
TOTAL                                 8234   1180    86%
```
**What to look for**:
- Overall coverage (must be ≥ 80%)
- Missing lines to identify untested code
- Decreases in coverage on changed files

### Test Failures
```
FAILED tests/unit/test_auth/test_manager.py::test_token_refresh - AssertionError
```
**What to do**:
1. Find the test file and function
2. Read the assertion message
3. Fix the code or test
4. Re-run: `uv run pytest tests/unit/test_auth/test_manager.py::test_token_refresh -v`

### Linting Errors
```
src/npm_mcp/server.py:45:1: F401 [*] `structlog` imported but unused
src/npm_mcp/server.py:78:80: E501 Line too long (105 > 100)
```
**What to do**:
1. Auto-fix with: `uv tool run ruff check --fix .`
2. Manual fixes for complex issues
3. Verify with: `uv tool run ruff check .`

### Type Errors
```
src/npm_mcp/auth/manager.py:45: error: Argument 1 has incompatible type "str | None"; expected "str"
```
**What to do**:
1. Add type guards:
   ```python
   if token is None:
       raise ValueError("Token required")
   process(token)  # Now mypy knows it's str
   ```
2. Or use type casting:
   ```python
   from typing import cast
   process(cast(str, token))
   ```

## Security Findings

### Hardcoded Secrets (CRITICAL)
```
src/npm_mcp/config.py:12: password = "admin123"
```
**Action**: MUST FIX IMMEDIATELY
```python
# Before (BAD)
password = "admin123"

# After (GOOD)
import os
password = os.environ["NPM_PASSWORD"]
```

### Dependency Vulnerabilities
```
cryptography 39.0.0 (vulnerability found, upgrade to ≥41.0.5)
```
**Action**:
```bash
# Check for vulnerabilities
pip-audit

# Upgrade specific package
uv pip install "cryptography>=41.0.5"

# Update lock file
uv lock
```

### Bandit Issues
```
B105: Possible hardcoded password: 'admin'
B602: Shell injection via subprocess.call with shell=True
```
**Action**:
```python
# Before (BAD)
subprocess.call(f"rm {filename}", shell=True)

# After (GOOD)
subprocess.call(["rm", filename], shell=False)
```

## Performance Tips

### Speed Up Local Tests
```bash
# Run only failed tests from last run
uv run pytest --lf

# Run tests in parallel (requires pytest-xdist)
uv run pytest -n auto

# Run specific test file
uv run pytest tests/unit/test_auth/test_manager.py

# Run tests matching pattern
uv run pytest -k "test_token"
```

### Speed Up CI Pipeline
1. Keep dependencies minimal
2. Use cache effectively (automatic)
3. Fix tests quickly (don't let them accumulate)
4. Run lint/format before pushing

## Artifact Locations

After pipeline runs, download from job artifacts:

| Artifact | Location | Purpose |
|----------|----------|---------|
| Coverage HTML | `htmlcov/index.html` | Visual coverage report |
| Coverage XML | `coverage.xml` | Machine-readable coverage |
| Ruff Report | `ruff-lint.json` | Linting violations |
| MyPy Report | `mypy-report.xml` | Type errors |
| Bandit Report | `bandit-report.json` | Security issues |
| pip-audit | `pip-audit-report.json` | Dependency vulnerabilities |

## Common Scenarios

### Scenario 1: Test Fails in CI, Passes Locally
**Possible causes**:
- Different Python version
- Missing dependency
- Environment-specific behavior

**Solution**:
```bash
# Test with exact CI Python version
docker run -it --rm -v $(pwd):/app python:3.11-slim-bookworm bash
cd /app
pip install uv
uv sync --all-extras
uv run pytest
```

### Scenario 2: Coverage Drops Below 80%
**Solution**:
```bash
# Find uncovered lines
uv run pytest --cov=src/npm_mcp --cov-report=html
open htmlcov/index.html

# Add tests for uncovered code
# OR temporarily lower threshold in pyproject.toml (not recommended)
```

### Scenario 3: Security Scan Finds Vulnerability
**Solution**:
```bash
# Check severity
pip-audit

# If high/critical: upgrade immediately
uv pip install "vulnerable-package>=fixed-version"
uv lock

# If low: plan upgrade in next sprint
# If false positive: document and create .pip-audit.toml exclusion
```

### Scenario 4: Linting Fails on Auto-Generated Code
**Solution**:
```python
# Add ruff ignore comment
# ruff: noqa: E501
very_long_line_that_cannot_be_shortened = "..."

# Or exclude file in pyproject.toml
[tool.ruff]
exclude = ["src/npm_mcp/generated/"]
```

### Scenario 5: Pipeline Timeout
**Possible causes**:
- Infinite loop in tests
- Slow network requests
- Large test suite

**Solution**:
```yaml
# Add timeout to job
test:py3.11:
  timeout: 10m  # Default is 1h
```

## Troubleshooting Checklist

### Before Asking for Help
- [ ] Read the complete error message
- [ ] Check job logs in GitLab UI
- [ ] Try reproducing locally
- [ ] Review recent changes
- [ ] Check if others have same issue
- [ ] Clear cache and retry

### When Creating Bug Report
Include:
1. Job name and stage
2. Full error message
3. Pipeline URL
4. Steps to reproduce
5. What you've tried
6. Relevant logs/artifacts

## GitLab UI Locations

### View Pipeline Results
1. Go to project
2. Click "CI/CD" > "Pipelines"
3. Click on pipeline number
4. Click on job to see logs

### View Coverage
1. Go to merge request
2. Check "Coverage" in MR widget
3. Or: "Analytics" > "Repository" > "Code coverage"

### View Security Findings
1. Go to "Security & Compliance" > "Vulnerability Report"
2. Filter by severity, scanner, status
3. Click finding for details and remediation

### Download Artifacts
1. Go to pipeline > job
2. Click "Browse" on right side
3. Download individual files or entire archive

### View Code Quality
1. Go to merge request
2. Click "Code Quality" tab
3. See inline annotations in diff

## Environment Variables

Set in GitLab: Settings > CI/CD > Variables

### Currently Used
- `CI` - Auto-set by GitLab
- `CI_PROJECT_DIR` - Auto-set by GitLab
- `CI_COMMIT_REF_SLUG` - Auto-set by GitLab

### Can Be Customized
```bash
# In GitLab UI: Settings > CI/CD > Variables
COVERAGE_MIN=85  # Increase coverage requirement
PYTEST_ARGS="-v --tb=short"  # More verbose output
```

## Links

- [Full Documentation](./CI_CD_PIPELINE.md)
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [Project Issues](https://github.com/wadew/npm-mcp/issues)

---

**Last Updated**: 2025-11-01
**Version**: 1.0
