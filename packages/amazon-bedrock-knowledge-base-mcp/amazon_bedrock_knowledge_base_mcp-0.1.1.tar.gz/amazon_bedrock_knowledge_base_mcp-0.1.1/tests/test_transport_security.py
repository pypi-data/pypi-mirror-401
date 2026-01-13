# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Tests for transport security configuration."""

from __future__ import annotations

from unittest.mock import patch

from amazon_bedrock_knowledge_base_mcp.app.factory import create_mcp_server
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig


def test_transport_security_warns_when_disabled(monkeypatch):
    """Disabling DNS rebinding protection via '*' should log a warning."""
    monkeypatch.setenv('MCP_ALLOWED_HOSTS', '*')
    monkeypatch.setenv('MCP_ALLOWED_ORIGINS', 'https://example.com')

    config = ServerConfig.from_env()
    with patch('amazon_bedrock_knowledge_base_mcp.app.factory.logger.warning') as warning:
        mcp = create_mcp_server(config=config)

    warning.assert_called_once()
    assert mcp.settings.transport_security is not None
    assert mcp.settings.transport_security.enable_dns_rebinding_protection is False
