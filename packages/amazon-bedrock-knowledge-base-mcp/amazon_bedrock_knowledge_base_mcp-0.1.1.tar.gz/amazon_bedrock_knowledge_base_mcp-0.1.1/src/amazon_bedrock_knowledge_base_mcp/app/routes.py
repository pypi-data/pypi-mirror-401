# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""HTTP routes for health checks."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

import boto3
from starlette.responses import JSONResponse

from amazon_bedrock_knowledge_base_mcp import __version__
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _check_json_file(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        json.load(f)


def _get_boto3_session(*, profile: str | None) -> boto3.Session:
    if profile:
        return boto3.Session(profile_name=profile)
    return boto3.Session()


def register_health_routes(mcp, *, config: ServerConfig) -> None:
    """Register `/health` and `/health/ready` routes on the MCP server."""

    @mcp.custom_route('/health', methods=['GET'])
    async def health(_request):
        return JSONResponse(
            {
                'status': 'ok',
                'timestamp': _now_iso(),
                'service': 'amazon-bedrock-knowledge-base-mcp',
                'version': __version__,
            }
        )

    @mcp.custom_route('/health/ready', methods=['GET'])
    async def health_ready(_request):
        try:
            if config.kb_schema_map_json_path:
                _check_json_file(config.kb_schema_map_json_path)
            if config.kb_schema_default_path:
                _check_json_file(config.kb_schema_default_path)

            region_name = config.aws_region or (os.getenv('AWS_DEFAULT_REGION') or None)
            sts = _get_boto3_session(profile=config.aws_profile).client(
                'sts', region_name=region_name
            )
            sts.get_caller_identity()
        except Exception as e:
            return JSONResponse(
                {
                    'status': 'not_ready',
                    'timestamp': _now_iso(),
                    'service': 'amazon-bedrock-knowledge-base-mcp',
                    'error': str(e),
                },
                status_code=503,
            )
        return JSONResponse(
            {
                'status': 'ready',
                'timestamp': _now_iso(),
                'service': 'amazon-bedrock-knowledge-base-mcp',
                'version': __version__,
            }
        )
