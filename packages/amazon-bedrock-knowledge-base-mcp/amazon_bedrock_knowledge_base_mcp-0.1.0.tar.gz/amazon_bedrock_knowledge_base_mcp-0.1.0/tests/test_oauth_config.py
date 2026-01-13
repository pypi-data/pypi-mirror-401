# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Tests for OAuth configuration.

OAuth enforcement is handled by `ServerConfig.from_env()`, and the MCP app factory wires auth into
FastMCP.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from amazon_bedrock_knowledge_base_mcp.app.factory import create_mcp_server
from amazon_bedrock_knowledge_base_mcp.auth.auth0 import Auth0JWTTokenVerifier
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig


def test_oauth_requires_streamable_http_transport(monkeypatch):
    """OAuth requires MCP_TRANSPORT=streamable-http."""
    monkeypatch.setenv('MCP_AUTH_MODE', 'oauth')
    monkeypatch.setenv('MCP_TRANSPORT', 'stdio')
    monkeypatch.setenv('AUTH0_DOMAIN', 'mytenant.us.auth0.com')
    monkeypatch.setenv('AUTH0_AUDIENCE', 'https://example.com/mcp')
    monkeypatch.setenv('MCP_RESOURCE_URL', 'https://example.com/mcp')

    with pytest.raises(ValueError, match='MCP_TRANSPORT=streamable-http'):
        ServerConfig.from_env()


def test_oauth_requires_domain_audience_and_resource_url(monkeypatch):
    """OAuth requires Auth0 env vars and MCP_RESOURCE_URL."""
    monkeypatch.setenv('MCP_AUTH_MODE', 'oauth')
    monkeypatch.setenv('MCP_TRANSPORT', 'streamable-http')
    monkeypatch.delenv('AUTH0_DOMAIN', raising=False)
    monkeypatch.delenv('AUTH0_AUDIENCE', raising=False)
    monkeypatch.delenv('MCP_RESOURCE_URL', raising=False)

    with pytest.raises(ValueError, match='AUTH0_DOMAIN is required'):
        ServerConfig.from_env()


def test_oauth_configures_fastmcp_auth(monkeypatch):
    """OAuth mode should configure FastMCP auth and token verification."""
    monkeypatch.setenv('MCP_AUTH_MODE', 'oauth')
    monkeypatch.setenv('MCP_TRANSPORT', 'streamable-http')
    monkeypatch.setenv('AUTH0_DOMAIN', 'mytenant.us.auth0.com')
    monkeypatch.setenv('AUTH0_AUDIENCE', 'https://example.com/mcp')
    monkeypatch.setenv('MCP_RESOURCE_URL', 'https://example.com/mcp')

    config = ServerConfig.from_env()
    mcp = create_mcp_server(config=config)
    assert mcp.settings.auth is not None
    assert str(mcp.settings.auth.issuer_url).rstrip('/') == 'https://mytenant.us.auth0.com'
    assert str(mcp.settings.auth.resource_server_url).rstrip('/') == 'https://example.com/mcp'
    assert isinstance(mcp._token_verifier, Auth0JWTTokenVerifier)


def test_oauth_rejects_invalid_resource_url(monkeypatch):
    """OAuth config should reject invalid MCP_RESOURCE_URL values at server creation time."""
    monkeypatch.setenv('MCP_AUTH_MODE', 'oauth')
    monkeypatch.setenv('MCP_TRANSPORT', 'streamable-http')
    monkeypatch.setenv('AUTH0_DOMAIN', 'mytenant.us.auth0.com')
    monkeypatch.setenv('AUTH0_AUDIENCE', 'https://example.com/mcp')
    monkeypatch.setenv('MCP_RESOURCE_URL', 'not-a-url')

    config = ServerConfig.from_env()
    with pytest.raises(ValidationError, match='valid URL'):
        create_mcp_server(config=config)
