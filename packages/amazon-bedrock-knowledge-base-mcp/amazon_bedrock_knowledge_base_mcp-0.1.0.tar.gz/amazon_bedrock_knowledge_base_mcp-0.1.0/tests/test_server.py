"""Tests for FastMCP wiring and CLI entrypoint.

The server implementation uses an app-factory pattern (no import-time env parsing or AWS client
construction). These tests validate:
1) tool registration via `create_mcp_server`, and
2) `main()` behavior via patching.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from amazon_bedrock_knowledge_base_mcp.app.factory import create_mcp_server
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig
from amazon_bedrock_knowledge_base_mcp.server import main


@pytest.mark.asyncio
async def test_create_mcp_server_registers_expected_tools(monkeypatch):
    """Register the public tool surface with stable names."""
    monkeypatch.delenv('MCP_AUTH_MODE', raising=False)
    monkeypatch.delenv('MCP_TRANSPORT', raising=False)
    config = ServerConfig.from_env()

    mcp = create_mcp_server(config=config)
    tools = await mcp.list_tools()
    assert {t.name for t in tools} == {
        'DescribeMetadataSchema',
        'ListKnowledgeBases',
        'QueryKnowledgeBases',
        'QueryKnowledgeBasesWithMetadata',
    }


def _minimal_config(*, transport: str) -> ServerConfig:
    return ServerConfig(
        aws_region=None,
        aws_profile=None,
        transport=transport,  # type: ignore[arg-type]
        host='127.0.0.1',
        port=8000,
        stateless_http=True,
        json_response=True,
        log_level='INFO',
        allowed_hosts_csv=None,
        allowed_origins_csv=None,
        auth_mode='none',
        auth0_domain=None,
        auth0_audience=None,
        mcp_resource_url=None,
        kb_inclusion_tag_key='mcp-multirag-kb',
        kb_search_type='DEFAULT',
        kb_reranking_enabled=False,
        kb_filter_mode='explicit_then_implicit',
        kb_allow_raw_filter=False,
        kb_schema_map_json_path=None,
        kb_schema_default_path=None,
        kb_implicit_filter_model_arn=None,
    )


def test_main_runs_stdio_by_default():
    """Run with stdio transport when config chooses it."""
    config = _minimal_config(transport='stdio')
    dummy_mcp = MagicMock()

    with patch(
        'amazon_bedrock_knowledge_base_mcp.server.ServerConfig.from_env', return_value=config
    ):
        with patch('amazon_bedrock_knowledge_base_mcp.server.configure_logging'):
            with patch(
                'amazon_bedrock_knowledge_base_mcp.server.create_mcp_server',
                return_value=dummy_mcp,
            ):
                main()

    dummy_mcp.run.assert_called_once_with()


def test_main_passes_transport_when_not_stdio():
    """Pass the requested transport to FastMCP.run()."""
    config = _minimal_config(transport='streamable-http')
    dummy_mcp = MagicMock()

    with patch(
        'amazon_bedrock_knowledge_base_mcp.server.ServerConfig.from_env', return_value=config
    ):
        with patch('amazon_bedrock_knowledge_base_mcp.server.configure_logging'):
            with patch(
                'amazon_bedrock_knowledge_base_mcp.server.create_mcp_server',
                return_value=dummy_mcp,
            ):
                main()

    dummy_mcp.run.assert_called_once_with(transport='streamable-http')
