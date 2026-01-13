# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Environment-driven configuration for the MCP server.

This module intentionally contains no side effects at import time.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal


McpTransport = Literal['stdio', 'sse', 'streamable-http']
McpAuthMode = Literal['none', 'oauth']
KnowledgeBaseSearchType = Literal['HYBRID', 'SEMANTIC', 'DEFAULT']
FilterMode = Literal['none', 'explicit_only', 'implicit_only', 'explicit_then_implicit']


def _parse_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    raw = value.strip().lower()
    if raw in ('true', '1', 'yes', 'on'):
        return True
    if raw in ('false', '0', 'no', 'off'):
        return False
    return default


def _parse_int(value: str | None, *, default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value.strip())
    except Exception:
        return default
    return parsed if parsed > 0 else default


def _parse_transport(value: str | None) -> McpTransport:
    raw = (value or 'stdio').strip().lower()
    if raw in ('stdio', 'sse', 'streamable-http'):
        return raw  # type: ignore[return-value]
    return 'stdio'


def _parse_search_type(value: str | None) -> KnowledgeBaseSearchType:
    raw = (value or 'DEFAULT').strip().upper()
    if raw in ('HYBRID', 'SEMANTIC', 'DEFAULT'):
        return raw  # type: ignore[return-value]
    return 'DEFAULT'


def _parse_filter_mode(value: str | None) -> FilterMode:
    raw = (value or 'explicit_then_implicit').strip().lower()
    if raw in ('none', 'explicit_only', 'implicit_only', 'explicit_then_implicit'):
        return raw  # type: ignore[return-value]
    return 'explicit_then_implicit'


def _parse_csv(value: str | None) -> str | None:
    if value is None:
        return None
    raw = value.strip()
    return raw if raw else ''


@dataclass(frozen=True, slots=True)
class ServerConfig:
    """Configuration for the Bedrock Knowledge Base MCP server."""

    # AWS
    aws_region: str | None
    aws_profile: str | None

    # MCP runtime
    transport: McpTransport
    host: str
    port: int
    stateless_http: bool
    json_response: bool
    log_level: str

    # MCP security
    allowed_hosts_csv: str | None
    allowed_origins_csv: str | None

    # Auth
    auth_mode: McpAuthMode
    auth0_domain: str | None
    auth0_audience: str | None
    mcp_resource_url: str | None

    # Knowledge base behavior
    kb_inclusion_tag_key: str
    kb_search_type: KnowledgeBaseSearchType
    kb_reranking_enabled: bool

    # Filtering / schema
    kb_filter_mode: FilterMode
    kb_allow_raw_filter: bool
    kb_schema_map_json_path: str | None
    kb_schema_default_path: str | None
    kb_implicit_filter_model_arn: str | None

    @classmethod
    def from_env(cls) -> 'ServerConfig':
        """Load configuration from environment variables.

        Raises:
            ValueError: If the environment contains an invalid configuration.
        """
        transport = _parse_transport(os.getenv('MCP_TRANSPORT'))
        host = (os.getenv('MCP_HOST') or '127.0.0.1').strip() or '127.0.0.1'
        port = _parse_int(os.getenv('PORT'), default=8000)
        stateless_http = _parse_bool(os.getenv('MCP_STATELESS'), default=True)

        auth_mode_raw = (os.getenv('MCP_AUTH_MODE') or 'none').strip().lower()
        auth_mode: McpAuthMode = 'none'
        if auth_mode_raw in ('none', 'oauth'):
            auth_mode = auth_mode_raw  # type: ignore[assignment]

        auth0_domain = os.getenv('AUTH0_DOMAIN')
        auth0_audience = os.getenv('AUTH0_AUDIENCE')
        mcp_resource_url = os.getenv('MCP_RESOURCE_URL')

        if auth_mode == 'oauth':
            if transport != 'streamable-http':
                raise ValueError(
                    'OAuth requires MCP_TRANSPORT=streamable-http for strict enforcement.'
                )
            if not auth0_domain:
                raise ValueError('AUTH0_DOMAIN is required when MCP_AUTH_MODE=oauth.')
            if not auth0_audience:
                raise ValueError('AUTH0_AUDIENCE is required when MCP_AUTH_MODE=oauth.')
            if not mcp_resource_url:
                raise ValueError('MCP_RESOURCE_URL is required when MCP_AUTH_MODE=oauth.')
            auth0_domain = auth0_domain.strip()
            auth0_audience = auth0_audience.strip()
            mcp_resource_url = mcp_resource_url.strip()

        kb_search_type = _parse_search_type(os.getenv('BEDROCK_KB_SEARCH_TYPE'))
        kb_reranking_enabled = _parse_bool(
            os.getenv('BEDROCK_KB_RERANKING_ENABLED'), default=False
        )
        kb_inclusion_tag_key = os.getenv('KB_INCLUSION_TAG_KEY') or 'mcp-multirag-kb'

        kb_filter_mode = _parse_filter_mode(os.getenv('BEDROCK_KB_FILTER_MODE'))
        kb_allow_raw_filter = _parse_bool(os.getenv('BEDROCK_KB_ALLOW_RAW_FILTER'), default=False)
        kb_schema_map_json_path = os.getenv('BEDROCK_KB_SCHEMA_MAP_JSON')
        kb_schema_default_path = os.getenv('BEDROCK_KB_SCHEMA_DEFAULT_PATH')
        kb_implicit_filter_model_arn = os.getenv('BEDROCK_KB_IMPLICIT_FILTER_MODEL_ARN')

        allowed_hosts_csv = _parse_csv(os.getenv('MCP_ALLOWED_HOSTS'))
        allowed_origins_csv = _parse_csv(os.getenv('MCP_ALLOWED_ORIGINS'))

        log_level = (
            os.getenv('LOG_LEVEL') or os.getenv('FASTMCP_LOG_LEVEL') or 'INFO'
        ).strip().upper() or 'INFO'

        json_response_default = transport == 'streamable-http'
        json_response = _parse_bool(os.getenv('MCP_JSON_RESPONSE'), default=json_response_default)

        return cls(
            aws_region=(os.getenv('AWS_REGION') or '').strip() or None,
            aws_profile=(os.getenv('AWS_PROFILE') or '').strip() or None,
            transport=transport,
            host=host,
            port=port,
            stateless_http=stateless_http,
            json_response=json_response,
            log_level=log_level,
            allowed_hosts_csv=allowed_hosts_csv,
            allowed_origins_csv=allowed_origins_csv,
            auth_mode=auth_mode,
            auth0_domain=auth0_domain,
            auth0_audience=auth0_audience,
            mcp_resource_url=mcp_resource_url,
            kb_inclusion_tag_key=kb_inclusion_tag_key,
            kb_search_type=kb_search_type,
            kb_reranking_enabled=kb_reranking_enabled,
            kb_filter_mode=kb_filter_mode,
            kb_allow_raw_filter=kb_allow_raw_filter,
            kb_schema_map_json_path=kb_schema_map_json_path,
            kb_schema_default_path=kb_schema_default_path,
            kb_implicit_filter_model_arn=kb_implicit_filter_model_arn,
        )
