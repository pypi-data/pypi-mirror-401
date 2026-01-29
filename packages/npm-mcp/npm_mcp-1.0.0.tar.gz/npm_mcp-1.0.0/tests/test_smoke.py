"""
Smoke test to verify the test infrastructure is working.

This file will be removed once Phase 1 implementation begins.
"""

import pytest

import npm_mcp
import npm_mcp.auth
import npm_mcp.client
import npm_mcp.config
import npm_mcp.models
import npm_mcp.tools
import npm_mcp.utils


def test_smoke_test() -> None:
    """
    Smoke test to verify pytest is configured correctly.

    This test ensures that:
    - pytest can discover and run tests
    - test infrastructure is set up properly
    - coverage tracking is working

    This test will be removed when Phase 1 implementation begins.
    """
    assert True  # Smoke test verifies test runner is working


def test_import_main_package() -> None:
    """Test that the main package can be imported."""
    assert hasattr(npm_mcp, "__version__")
    assert npm_mcp.__version__ == "1.0.0"


def test_import_subpackages() -> None:
    """Test that all subpackages can be imported."""
    # Just verify the imports worked (imports are at module level)
    assert npm_mcp.auth is not None
    assert npm_mcp.client is not None
    assert npm_mcp.config is not None
    assert npm_mcp.models is not None
    assert npm_mcp.tools is not None
    assert npm_mcp.utils is not None


@pytest.mark.asyncio
async def test_async_infrastructure() -> None:
    """
    Test that async test infrastructure is working.

    This verifies that pytest-asyncio is configured correctly.
    """

    # Simple async test
    async def dummy_async_function() -> str:
        return "async works"

    result = await dummy_async_function()
    assert result == "async works"
