# GitLab CI/CD Pipeline Documentation

## Overview

The npm_mcp project uses a comprehensive GitLab CI/CD pipeline to ensure code quality, security, and reliability. The pipeline runs automatically on every commit and merge request.

**Pipeline Version**: 2.0
**Last Updated**: 2025-11-01

## Pipeline Architecture

The pipeline consists of 3 main stages that run in parallel where possible for optimal performance:

```
┌─────────────────────────────────────────────────────────────┐
│                        STAGE 1: TEST                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Python 3.11  │  │ Python 3.12  │  │ Python 3.13  │      │
│  │   (Primary)  │  │ (Allow Fail) │  │ (Allow Fail) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        STAGE 2: LINT                         │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ Ruff Linting │  │ MyPy Types   │                         │
│  │  & Formatting│  │ (Allow Fail) │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      STAGE 3: SECURITY                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ GitLab SAST  │  │ Secret Scan  │  │ Dependency   │      │
│  │              │  │              │  │  Scanning    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ Credentials  │  │  pip-audit   │  Bandit SAST   │      │
│  │   Scanner    │  │ (Allow Fail) │  (Allow Fail)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Stage Details

### Stage 1: Testing

**Purpose**: Run the test suite across multiple Python versions with coverage reporting.

**Jobs**:
- `test:py3.11` - Primary Python version (MUST PASS)
- `test:py3.12` - Compatibility check (can fail)
- `test:py3.13` - Compatibility check (can fail)

**Success Criteria**:
- All tests pass in Python 3.11 job
- Code coverage ≥ 80%
- No critical test failures

**Artifacts**:
- `coverage.xml` - Cobertura coverage report
- `htmlcov/` - HTML coverage report
- `junit.xml` - JUnit test results

**Coverage Report**:
The pipeline extracts and displays coverage percentage in the GitLab UI. You can view:
- Line-by-line coverage in MR diff view
- Coverage trend over time in the project analytics
- Detailed HTML report in job artifacts

**Optimization**:
- Uses `uv` for fast dependency installation (5-10x faster than pip)
- Caches dependencies based on `pyproject.toml` and `uv.lock`
- Parallel execution across Python versions

### Stage 2: Linting

**Purpose**: Enforce code quality and style standards.

**Jobs**:

#### `lint:ruff`
- **Checks**: Code linting, formatting, import sorting
- **Output**: GitLab Code Quality report
- **Must Pass**: Yes
- **Configuration**: `pyproject.toml` (tool.ruff section)

**Common Failures**:
- Import sorting violations (use `ruff check --fix .` locally)
- Formatting issues (use `ruff format .` locally)
- Code style violations (review ruff-lint.json artifact)

#### `lint:mypy`
- **Checks**: Static type checking
- **Output**: JUnit XML report
- **Must Pass**: No (allow_failure: true)
- **Configuration**: `pyproject.toml` (tool.mypy section)

**Common Warnings**:
- Missing type annotations
- Type incompatibilities
- Import resolution issues

**Optimization**:
- Runs in parallel with test stage (DAG optimization with `needs: []`)
- Pull-only cache (doesn't modify dependencies)
- Uses `uv tool run` for isolated tool execution

### Stage 3: Security

**Purpose**: Identify security vulnerabilities, secrets, and dependency issues.

**Jobs**:

#### `semgrep-sast` (GitLab SAST)
- **Type**: Static Application Security Testing
- **Engine**: Semgrep
- **Coverage**: Python security patterns, OWASP Top 10
- **Output**: Security Dashboard, SAST report
- **Configuration**: GitLab-managed template

**What it finds**:
- SQL injection vulnerabilities
- Command injection risks
- Insecure cryptography usage
- Path traversal vulnerabilities
- XSS risks (if applicable)

#### `secret_detection` (GitLab Secret Detection)
- **Type**: Secrets Scanning
- **Engine**: GitLab Secret Detection
- **Coverage**: 100+ secret patterns
- **Output**: Security Dashboard

**What it finds**:
- AWS credentials
- API keys and tokens
- Private keys
- Database passwords
- OAuth tokens

#### `gemnasium-python-dependency_scanning` (GitLab Dependency Scanning)
- **Type**: Software Composition Analysis (SCA)
- **Engine**: Gemnasium
- **Coverage**: Known vulnerabilities in dependencies (CVE database)
- **Output**: Security Dashboard, Dependency report

**What it finds**:
- Known CVEs in Python packages
- Outdated dependencies with security patches
- License compliance issues

#### `security:credentials` (Custom Scanner)
- **Type**: Hardcoded Credentials Detection
- **Engine**: ripgrep pattern matching
- **Must Pass**: Yes
- **Patterns Checked**:
  - Password assignments: `password = "..."`
  - API keys: `api_key = "..."`
  - Tokens: `token = "..."`
  - Secrets: `secret = "..."`
  - Private keys: `BEGIN PRIVATE KEY`

**Failure Action**: Pipeline fails if patterns are detected in `src/` directory.

#### `security:pip-audit` (Python Dependency Audit)
- **Type**: Dependency Vulnerability Scanning
- **Engine**: pip-audit (PyPA official tool)
- **Output**: JSON vulnerability report
- **Must Pass**: No (allow_failure: true for low-severity)

**What it finds**:
- Known vulnerabilities from OSV database
- Severity levels (low, medium, high, critical)
- Available patches and fixes

#### `security:bandit` (Python SAST)
- **Type**: Python-specific security analysis
- **Engine**: Bandit (PyCQA official tool)
- **Output**: GitLab Code Quality report
- **Must Pass**: No (allow_failure: true)
- **Configuration**: `.bandit` file

**What it finds**:
- Hardcoded passwords (B105, B106)
- Use of `eval()` and `exec()` (B307)
- Insecure temp file usage (B108)
- SQL injection risks (B608)
- Shell injection (B602, B603)
- Weak cryptography (B303, B304, B305)

**Optimization**:
- All security jobs run in parallel (`needs: []`)
- GitLab-managed scanners use pre-built images
- Results cached in Security Dashboard for tracking

## Pipeline Triggers

The pipeline runs automatically on:

1. **Merge Requests**: Full pipeline on every MR commit
2. **Main Branch**: Full pipeline on every commit to default branch
3. **Tags**: Full pipeline on Git tags

**Duplicate Prevention**: Prevents duplicate pipelines when both branch and MR exist.

## Caching Strategy

The pipeline uses intelligent caching to speed up builds:

### Cache Key
```yaml
key:
  files:
    - pyproject.toml
    - uv.lock
  prefix: ${CI_COMMIT_REF_SLUG}
```

**Cache invalidation**: Automatic when dependencies change.

### Cached Paths
- `.cache/pip` - pip package cache
- `.cache/uv` - uv package cache
- `.venv/` - Virtual environment

### Cache Policies
- **pull-push**: Test jobs (may install new dependencies)
- **pull**: Lint/security jobs (read-only, faster)

### Expected Performance
- **First run**: 2-3 minutes (cold cache)
- **Subsequent runs**: 30-60 seconds (warm cache)
- **Dependency change**: 1-2 minutes (partial cache hit)

## Running the Pipeline Locally

### Prerequisites
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras
```

### Run Tests Locally
```bash
# Run full test suite with coverage
uv run pytest --cov=src/npm_mcp --cov-report=term-missing --cov-report=html

# Check coverage threshold
uv run coverage report --fail-under=80

# Run specific test file
uv run pytest tests/unit/test_auth/test_manager.py -v

# Run with specific markers
uv run pytest -m "unit" -v
```

### Run Linting Locally
```bash
# Ruff linting
uv tool install ruff
uv tool run ruff check .

# Auto-fix linting issues
uv tool run ruff check --fix .

# Format code
uv tool run ruff format .

# Check formatting without changes
uv tool run ruff format --check .

# MyPy type checking
uv run mypy src/
```

### Run Security Scans Locally
```bash
# Install security tools
pip install bandit[toml] pip-audit

# Bandit SAST
bandit -r src/ -f screen

# pip-audit dependency scan
pip-audit --format=markdown

# Custom credential scan (requires ripgrep)
rg -i 'password\s*=\s*["\047][^"\047]{3,}["\047]' src/
```

### Simulate CI Environment
```bash
# Set CI environment variables
export CI=true
export CI_PROJECT_DIR=$(pwd)
export PYTEST_ARGS="-ra --strict-markers --strict-config"
export COVERAGE_MIN=80

# Run tests as CI does
uv run pytest $PYTEST_ARGS --cov=src/npm_mcp --cov-report=term-missing --cov-report=xml
uv run coverage report --fail-under=$COVERAGE_MIN
```

## Interpreting Results

### Test Results

**Success Indicators**:
- ✅ Green checkmark on test jobs
- Coverage percentage displayed in MR widget
- All 762+ tests passing

**Failure Analysis**:
1. Click on failed test job
2. Scroll to "FAILURES" section in logs
3. Review stack trace and assertion errors
4. Download JUnit XML for detailed analysis

**Coverage Analysis**:
1. Download `htmlcov/` artifact
2. Open `htmlcov/index.html` in browser
3. Click on files with low coverage
4. Review highlighted lines (red = not covered, green = covered)

### Linting Results

**Ruff Violations**:
- View in GitLab Code Quality tab
- Download `ruff-lint.json` artifact
- Severity levels: error, warning, info

**Common Fixes**:
```bash
# Auto-fix most issues
ruff check --fix .

# Format all files
ruff format .

# Check specific file
ruff check src/npm_mcp/server.py
```

**MyPy Type Errors**:
- View in Test Reports tab (JUnit)
- Download `mypy-report.xml` artifact
- Errors show file, line number, and description

**Common Fixes**:
```python
# Add type hints
def process_data(data: dict[str, Any]) -> list[str]:
    ...

# Use type ignores sparingly
result = some_function()  # type: ignore[no-untyped-call]
```

### Security Results

**Security Dashboard** (GitLab Ultimate/Premium):
- Navigate to Security & Compliance > Vulnerability Report
- View all findings across SAST, Secret Detection, Dependency Scanning
- Filter by severity, status, scanner
- Create issues from findings

**SAST Findings**:
- **Critical/High**: Must fix before merge
- **Medium**: Review and fix or justify
- **Low/Info**: Optional improvements

**Secret Detection**:
- **Any finding**: MUST FIX (security critical)
- Remove secret from code and history
- Rotate the exposed credential
- Use GitLab CI/CD variables or environment variables

**Dependency Vulnerabilities**:
- **Critical**: Upgrade immediately
- **High**: Plan upgrade in current sprint
- **Medium/Low**: Include in next maintenance cycle

**Custom Credential Scanner**:
- **Failure**: Hardcoded secrets found in `src/`
- **Action**: Move to environment variables or GitLab CI/CD variables
- **Configuration**: Use `config/` files with `.gitignore`

**Bandit Findings**:
- Download `bandit-report.json` for full details
- Review Code Quality tab for inline annotations
- Common issues:
  - B105: Hardcoded password (use environment variables)
  - B602: Shell injection (use `shlex.quote()` or `subprocess` with list)
  - B608: SQL injection (use parameterized queries)

**pip-audit Findings**:
- Download `pip-audit-report.json`
- View vulnerabilities with CVE IDs
- Check for available fixes:
  ```bash
  pip-audit --fix --dry-run
  uv pip install <package>==<fixed-version>
  ```

## Artifacts

All job artifacts are stored for 7 days and can be downloaded from the pipeline view.

### Test Artifacts
- `coverage.xml` - Machine-readable coverage (Cobertura format)
- `htmlcov/` - Human-readable HTML coverage report
- `junit.xml` - Test results in JUnit format
- `.coverage` - Raw coverage data file

### Linting Artifacts
- `ruff-lint.json` - GitLab Code Quality format
- `mypy-report.xml` - JUnit XML format

### Security Artifacts
- `bandit-report.json` - Bandit findings (JSON)
- `bandit-codequality.json` - GitLab Code Quality format
- `pip-audit-report.json` - pip-audit vulnerabilities

## Troubleshooting

### Pipeline Fails to Start

**Issue**: Pipeline doesn't trigger on commit/MR

**Solutions**:
1. Check `.gitlab-ci.yml` syntax:
   ```bash
   # In GitLab UI: CI/CD > Editor > Validate
   ```
2. Verify workflow rules match your scenario
3. Check GitLab CI/CD settings are enabled

### Test Job Fails with "ModuleNotFoundError"

**Issue**: Tests can't import npm_mcp modules

**Solution**:
```bash
# Ensure uv sync runs successfully
uv sync --all-extras

# Check that src/ is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Coverage Below Threshold

**Issue**: Coverage drops below 80%

**Solution**:
1. Download `htmlcov/` artifact
2. Identify uncovered lines
3. Add tests for uncovered code
4. Or adjust threshold in `pyproject.toml`:
   ```toml
   [tool.pytest.ini_options]
   addopts = ["--cov-fail-under=75"]  # Temporary reduction
   ```

### Cache Issues

**Issue**: Pipeline is slow despite caching

**Solutions**:
1. Clear cache in GitLab: CI/CD > Pipelines > Clear Runner Caches
2. Verify `uv.lock` is committed
3. Check cache key matches across jobs
4. Ensure `.cache/` directories exist

### Security Scanner False Positives

**Issue**: Bandit reports false positives

**Solution**:
1. Add inline exception:
   ```python
   password = get_from_env()  # nosec B105
   ```
2. Configure in `.bandit`:
   ```ini
   [bandit]
   skips = B105,B106
   ```
3. Document in MR why it's safe

### "uv not found" Error

**Issue**: Job fails with `uv: command not found`

**Solution**:
- Ensure `before_script` includes:
  ```yaml
  before_script:
    - pip install uv
  ```

### MyPy Import Errors

**Issue**: MyPy can't resolve imports

**Solutions**:
1. Check `[tool.mypy.overrides]` in `pyproject.toml`
2. Add to overrides:
   ```toml
   [[tool.mypy.overrides]]
   module = "problematic_module.*"
   ignore_missing_imports = true
   ```
3. Install type stubs:
   ```bash
   uv pip install types-<package>
   ```

## Performance Optimization

### Current Performance (as of 2025-11-01)
- **Cold cache**: ~2-3 minutes
- **Warm cache**: ~30-60 seconds
- **Test stage**: ~15-30 seconds per Python version
- **Lint stage**: ~10-20 seconds
- **Security stage**: ~30-60 seconds

### Optimization Tips

1. **Parallelize Independent Jobs**:
   ```yaml
   job_name:
     needs: []  # Don't wait for previous stages
   ```

2. **Use Interruptible Jobs**:
   ```yaml
   job_name:
     interruptible: true  # Cancel if new commit pushed
   ```

3. **Optimize Test Selection**:
   ```bash
   # Run only changed tests (requires pytest-picked)
   pytest --picked
   ```

4. **Split Test Jobs**:
   ```yaml
   test:unit:
     script: pytest tests/unit/

   test:integration:
     script: pytest tests/integration/
   ```

5. **Use Slim Docker Images**:
   - Current: `python:3.11-slim-bookworm` (130 MB)
   - Alternative: `python:3.11-alpine` (50 MB, may have compatibility issues)

## CI/CD Variables

Configure these in GitLab: Settings > CI/CD > Variables

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COVERAGE_MIN` | Minimum coverage threshold | `80` |
| `PYTEST_ARGS` | Additional pytest arguments | `-ra --strict-markers` |
| `UV_NO_PROGRESS` | Disable uv progress bars | `1` |
| `SAST_EXCLUDED_PATHS` | Paths to exclude from SAST | `tests/,examples/` |

### For Future Deployment (Not Used Currently)

| Variable | Description | Required |
|----------|-------------|----------|
| `PYPI_TOKEN` | PyPI API token for publishing | No |
| `DOCKER_HUB_USERNAME` | Docker Hub username | No |
| `DOCKER_HUB_TOKEN` | Docker Hub access token | No |

## Best Practices

### For Developers

1. **Run tests locally before pushing**:
   ```bash
   uv run pytest --cov=src/npm_mcp
   ```

2. **Fix linting issues before committing**:
   ```bash
   uv tool run ruff check --fix .
   uv tool run ruff format .
   ```

3. **Review security findings immediately**:
   - Don't commit secrets
   - Update vulnerable dependencies
   - Address SAST findings

4. **Write tests for new code**:
   - Maintain 80%+ coverage
   - Include edge cases
   - Add integration tests for features

5. **Use descriptive commit messages**:
   ```
   feat: add new authentication method
   fix: resolve token expiration bug
   test: add coverage for edge case
   ```

### For Code Reviewers

1. **Check pipeline status before review**
2. **Review Code Quality tab for linting issues**
3. **Check Security tab for new vulnerabilities**
4. **Verify coverage didn't decrease**
5. **Ensure all required jobs passed**

### For Maintainers

1. **Monitor Security Dashboard weekly**
2. **Keep dependencies updated**:
   ```bash
   uv lock --upgrade
   ```
3. **Review and update security rules quarterly**
4. **Track coverage trends over time**
5. **Optimize pipeline performance as needed**

## Getting Help

### Pipeline Failing?

1. **Check the logs**: Click on failed job, read error output
2. **Download artifacts**: Useful for detailed debugging
3. **Run locally**: Reproduce the failure on your machine
4. **Search GitLab docs**: [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
5. **Ask for help**: Create an issue with:
   - Job name and failure message
   - Pipeline URL
   - Steps to reproduce

### Need to Modify Pipeline?

1. **Edit `.gitlab-ci.yml`**
2. **Validate syntax**: Use GitLab CI Lint tool
3. **Test in feature branch**: Push and verify
4. **Document changes**: Update this file
5. **Create MR**: Get review before merging

### Security Questions?

1. **Review finding details** in Security Dashboard
2. **Check CVE databases** for vulnerability info
3. **Consult security team** for critical issues
4. **Document exceptions** with justification
5. **Schedule remediation** in sprint planning

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Bandit Security Scanner](https://bandit.readthedocs.io/)
- [pip-audit](https://pypi.org/project/pip-audit/)
- [GitLab Security Scanners](https://docs.gitlab.com/ee/user/application_security/)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-01
**Maintained By**: npm_mcp Team
