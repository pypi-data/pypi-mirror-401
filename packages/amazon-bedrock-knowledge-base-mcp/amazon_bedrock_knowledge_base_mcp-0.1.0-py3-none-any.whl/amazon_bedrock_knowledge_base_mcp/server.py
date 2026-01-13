# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""CLI entry point for the Amazon Bedrock Knowledge Base MCP server.

This module is intentionally side-effect-free at import time. Use `main()` to run the server.
"""

from __future__ import annotations

from loguru import logger

from amazon_bedrock_knowledge_base_mcp.app.factory import create_mcp_server
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig
from amazon_bedrock_knowledge_base_mcp.core.logging import configure_logging


def main() -> None:
    """Run the MCP server based on environment configuration."""
    config = ServerConfig.from_env()
    configure_logging(level=config.log_level)

    logger.info(
        f'MCP runtime: transport={config.transport} host={config.host} port={config.port} '
        f'stateless_http={config.stateless_http} json_response={config.json_response}'
    )
    logger.info(f'Auth mode: {config.auth_mode} (from MCP_AUTH_MODE)')
    logger.info(f'Default search type: {config.kb_search_type} (from BEDROCK_KB_SEARCH_TYPE)')
    logger.info(
        f'Raw filter passthrough enabled: {config.kb_allow_raw_filter} '
        f'(from BEDROCK_KB_ALLOW_RAW_FILTER)'
    )
    logger.info(f'Default filter mode: {config.kb_filter_mode} (from BEDROCK_KB_FILTER_MODE)')
    logger.info(
        f'Default reranking enabled: {config.kb_reranking_enabled} '
        f'(from BEDROCK_KB_RERANKING_ENABLED)'
    )

    mcp = create_mcp_server(config=config)
    if config.transport == 'stdio':
        mcp.run()
        return
    mcp.run(transport=config.transport)


if __name__ == '__main__':
    main()
