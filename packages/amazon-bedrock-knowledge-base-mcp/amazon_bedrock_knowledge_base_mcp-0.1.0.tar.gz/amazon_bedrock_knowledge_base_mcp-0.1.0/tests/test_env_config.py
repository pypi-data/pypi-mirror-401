# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Tests for environment-driven configuration.

The server uses a side-effect-free app-factory pattern: environment variables are parsed only when
`ServerConfig.from_env()` is called.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from amazon_bedrock_knowledge_base_mcp.app.factory import create_mcp_server
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig


@pytest.mark.parametrize('value', ['true', '1', 'yes', 'on'])
def test_reranking_enabled_truthy_values(monkeypatch, value: str):
    """Parse truthy values for BEDROCK_KB_RERANKING_ENABLED."""
    monkeypatch.setenv('BEDROCK_KB_RERANKING_ENABLED', value)
    config = ServerConfig.from_env()
    assert config.kb_reranking_enabled is True


@pytest.mark.parametrize('value', ['false', '0', 'no', 'off'])
def test_reranking_disabled_falsy_values(monkeypatch, value: str):
    """Parse falsy values for BEDROCK_KB_RERANKING_ENABLED."""
    monkeypatch.setenv('BEDROCK_KB_RERANKING_ENABLED', value)
    config = ServerConfig.from_env()
    assert config.kb_reranking_enabled is False


def test_reranking_defaults_to_off(monkeypatch):
    """Default to reranking disabled when env var is unset."""
    monkeypatch.delenv('BEDROCK_KB_RERANKING_ENABLED', raising=False)
    config = ServerConfig.from_env()
    assert config.kb_reranking_enabled is False


def test_search_type_defaults_to_default(monkeypatch):
    """Default to BEDROCK_KB_SEARCH_TYPE=DEFAULT when env var is unset."""
    monkeypatch.delenv('BEDROCK_KB_SEARCH_TYPE', raising=False)
    config = ServerConfig.from_env()
    assert config.kb_search_type == 'DEFAULT'


def test_search_type_can_be_set_to_hybrid(monkeypatch):
    """Parse BEDROCK_KB_SEARCH_TYPE=HYBRID."""
    monkeypatch.setenv('BEDROCK_KB_SEARCH_TYPE', 'HYBRID')
    config = ServerConfig.from_env()
    assert config.kb_search_type == 'HYBRID'


@pytest.mark.asyncio
async def test_query_tool_default_values_come_from_config(monkeypatch):
    """Tool parameter defaults should reflect the config used to build the server."""
    monkeypatch.setenv('BEDROCK_KB_RERANKING_ENABLED', 'true')
    monkeypatch.setenv('BEDROCK_KB_SEARCH_TYPE', 'HYBRID')
    config = ServerConfig.from_env()

    mocked = AsyncMock(return_value='ok')
    with patch('amazon_bedrock_knowledge_base_mcp.app.factory.query_knowledge_bases', new=mocked):
        mcp = create_mcp_server(config=config)
        await mcp.call_tool(
            'QueryKnowledgeBases',
            {'query': 'q', 'knowledge_base_id': 'kb', 'number_of_results': 10},
        )

    assert mocked.await_count == 1
    assert mocked.await_args is not None
    kwargs = mocked.await_args.kwargs
    assert kwargs['reranking'] is True
    assert kwargs['search_type'] == 'HYBRID'


@pytest.mark.asyncio
async def test_query_tool_explicit_params_override_defaults(monkeypatch):
    """Explicit call args override the defaults captured from config."""
    monkeypatch.setenv('BEDROCK_KB_RERANKING_ENABLED', 'true')
    monkeypatch.setenv('BEDROCK_KB_SEARCH_TYPE', 'HYBRID')
    config = ServerConfig.from_env()

    mocked = AsyncMock(return_value='ok')
    with patch('amazon_bedrock_knowledge_base_mcp.app.factory.query_knowledge_bases', new=mocked):
        mcp = create_mcp_server(config=config)
        await mcp.call_tool(
            'QueryKnowledgeBases',
            {
                'query': 'q',
                'knowledge_base_id': 'kb',
                'number_of_results': 10,
                'reranking': False,
                'search_type': 'DEFAULT',
            },
        )

    assert mocked.await_args is not None
    kwargs = mocked.await_args.kwargs
    assert kwargs['reranking'] is False
    assert kwargs['search_type'] == 'DEFAULT'
