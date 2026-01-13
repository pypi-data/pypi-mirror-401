# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Core service logic for the MCP tools.

This module contains the business logic used by the MCP tools, separated from the FastMCP
registration layer to keep imports side-effect-free and tests straightforward.
"""

from __future__ import annotations

import json
from typing import Any, Literal

from amazon_bedrock_knowledge_base_mcp.aws.provider import BedrockClientsProvider
from amazon_bedrock_knowledge_base_mcp.core.config import (
    FilterMode,
    KnowledgeBaseSearchType,
    ServerConfig,
)
from amazon_bedrock_knowledge_base_mcp.kb.discovery import discover_knowledge_bases
from amazon_bedrock_knowledge_base_mcp.kb.filters import (
    FilterError,
    build_where_filter,
    combine_filters_and,
    validate_raw_filter_against_schema,
)
from amazon_bedrock_knowledge_base_mcp.kb.retrieval import query_knowledge_base
from amazon_bedrock_knowledge_base_mcp.kb.schema import (
    MetadataSchemaFile,
    ResolvedSchema,
    SchemaMode,
    SchemaSource,
    auto_discover_schema_from_results,
    log_schema_summary,
    resolve_schema_for_kb,
    schema_to_implicit_metadata_attributes,
)


def _auto_discover_schema(
    *,
    provider: BedrockClientsProvider,
    knowledge_base_id: str,
    sample_query: str,
    sample_k: int,
) -> MetadataSchemaFile:
    runtime_client, _agent_client = provider.get_clients()
    response = runtime_client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={'text': sample_query},
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': sample_k,
            }
        },
    )
    results = response.get('retrievalResults') or []
    if not isinstance(results, list):
        results = []
    return auto_discover_schema_from_results(results)


def _resolve_schema(
    *,
    config: ServerConfig,
    provider: BedrockClientsProvider,
    schema_cache: dict[str, tuple[MetadataSchemaFile, SchemaSource]],
    knowledge_base_id: str,
    metadata_schema_mode: SchemaMode,
    metadata_schema_auto_sample_query: str,
    metadata_schema_auto_sample_k: int,
) -> ResolvedSchema:
    resolved = resolve_schema_for_kb(
        knowledge_base_id=knowledge_base_id,
        schema_mode=metadata_schema_mode,
        schema_map_json_path=config.kb_schema_map_json_path,
        schema_default_path=config.kb_schema_default_path,
        schema_cache=schema_cache,
        auto_discover_fn=lambda: _auto_discover_schema(
            provider=provider,
            knowledge_base_id=knowledge_base_id,
            sample_query=metadata_schema_auto_sample_query,
            sample_k=metadata_schema_auto_sample_k,
        ),
    )
    log_schema_summary(resolved.schema, knowledge_base_id)
    return resolved


def _build_implicit_filter_configuration(
    *,
    config: ServerConfig,
    schema: MetadataSchemaFile,
) -> dict[str, Any]:
    if not config.kb_implicit_filter_model_arn:
        raise ValueError(
            'Implicit filtering requires BEDROCK_KB_IMPLICIT_FILTER_MODEL_ARN to be set.'
        )
    metadata_attributes = schema_to_implicit_metadata_attributes(schema)
    if not metadata_attributes:
        raise ValueError('No usable metadata attributes available for implicit filtering.')
    return {
        'metadataAttributes': metadata_attributes,
        'modelArn': config.kb_implicit_filter_model_arn,
    }


async def describe_metadata_schema(
    *,
    config: ServerConfig,
    provider: BedrockClientsProvider,
    schema_cache: dict[str, tuple[MetadataSchemaFile, SchemaSource]],
    knowledge_base_id: str,
    metadata_schema_mode: SchemaMode,
    metadata_schema_auto_sample_query: str,
    metadata_schema_auto_sample_k: int,
) -> str:
    """Return the effective metadata schema for a knowledge base."""
    resolved = _resolve_schema(
        config=config,
        provider=provider,
        schema_cache=schema_cache,
        knowledge_base_id=knowledge_base_id,
        metadata_schema_mode=metadata_schema_mode,
        metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
        metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
    )
    return json.dumps(
        {
            'knowledge_base_id': knowledge_base_id,
            'schema_source': resolved.source,
            'cache_hit': resolved.cache_hit,
            'schema': resolved.schema.model_dump(),
        }
    )


async def list_knowledge_bases(*, config: ServerConfig, provider: BedrockClientsProvider) -> str:
    """List available knowledge bases and their data sources."""
    _runtime_client, agent_client = provider.get_clients()
    knowledge_bases = await discover_knowledge_bases(agent_client, config.kb_inclusion_tag_key)
    return json.dumps(knowledge_bases)


async def query_knowledge_bases(
    *,
    config: ServerConfig,
    provider: BedrockClientsProvider,
    schema_cache: dict[str, tuple[MetadataSchemaFile, SchemaSource]],
    query: str,
    knowledge_base_id: str,
    number_of_results: int,
    reranking: bool,
    reranking_model_name: Literal['COHERE', 'AMAZON'],
    data_source_ids: list[str] | None,
    search_type: KnowledgeBaseSearchType,
    filter_mode: FilterMode,
    where_join: Literal['AND', 'OR'],
    where: dict[str, Any] | None,
    raw_filter: dict[str, Any] | None,
    implicit_filter: bool,
    metadata_schema_mode: SchemaMode,
    metadata_schema_auto_sample_query: str,
    metadata_schema_auto_sample_k: int,
) -> str:
    """Query a knowledge base and return matching passages."""
    needs_schema = where is not None or raw_filter is not None or implicit_filter

    resolved_schema = None
    if needs_schema:
        resolved_schema = _resolve_schema(
            config=config,
            provider=provider,
            schema_cache=schema_cache,
            knowledge_base_id=knowledge_base_id,
            metadata_schema_mode=metadata_schema_mode,
            metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
            metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
        )

    if raw_filter is not None:
        if not config.kb_allow_raw_filter:
            raise ValueError(
                'Raw filter passthrough is disabled. Set BEDROCK_KB_ALLOW_RAW_FILTER=true to enable.'
            )
        if resolved_schema is None:
            raise ValueError(
                'Raw filters require a resolved metadata schema. Provide a schema via env vars or enable auto mode.'
            )
        validation = validate_raw_filter_against_schema(
            schema=resolved_schema.schema,
            raw_filter=raw_filter,
        )
        if not validation.ok:
            raise ValueError(validation.error or 'Raw filter validation failed.')

    where_filter = None
    if resolved_schema is not None:
        try:
            where_filter = build_where_filter(
                schema=resolved_schema.schema,
                where=where,
                where_join=where_join,
            )
        except FilterError as e:
            raise ValueError(str(e)) from e

    explicit_filter = combine_filters_and([where_filter, raw_filter])

    implicit_filter_configuration = None
    if filter_mode in ('implicit_only', 'explicit_then_implicit') and implicit_filter:
        if resolved_schema is None:
            resolved_schema = _resolve_schema(
                config=config,
                provider=provider,
                schema_cache=schema_cache,
                knowledge_base_id=knowledge_base_id,
                metadata_schema_mode=metadata_schema_mode,
                metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
                metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
            )
        implicit_filter_configuration = _build_implicit_filter_configuration(
            config=config,
            schema=resolved_schema.schema,
        )

    retrieval_filter = None
    if filter_mode == 'explicit_only':
        retrieval_filter = explicit_filter
    elif filter_mode == 'implicit_only':
        retrieval_filter = None
    elif filter_mode == 'explicit_then_implicit':
        retrieval_filter = explicit_filter

    runtime_client, _agent_client = provider.get_clients()
    return await query_knowledge_base(
        query=query,
        knowledge_base_id=knowledge_base_id,
        kb_agent_client=runtime_client,
        number_of_results=number_of_results,
        reranking=reranking,
        reranking_model_name=reranking_model_name,
        data_source_ids=data_source_ids,
        search_type=search_type,
        include_metadata=False,
        retrieval_filter=retrieval_filter,
        implicit_filter_configuration=implicit_filter_configuration,
    )


async def query_knowledge_bases_with_metadata(
    *,
    config: ServerConfig,
    provider: BedrockClientsProvider,
    schema_cache: dict[str, tuple[MetadataSchemaFile, SchemaSource]],
    query: str,
    knowledge_base_id: str,
    number_of_results: int | None,
    reranking: bool,
    reranking_model_name: Literal['COHERE', 'AMAZON'],
    data_source_ids: list[str] | None,
    content_max_chars: int | None,
    search_type: KnowledgeBaseSearchType,
    filter_mode: FilterMode,
    where_join: Literal['AND', 'OR'],
    where: dict[str, Any] | None,
    raw_filter: dict[str, Any] | None,
    implicit_filter: bool,
    metadata_schema_mode: SchemaMode,
    metadata_schema_auto_sample_query: str,
    metadata_schema_auto_sample_k: int,
) -> str:
    """Query a knowledge base and include Bedrock metadata per result."""
    effective_num_results = number_of_results
    if effective_num_results is None:
        effective_num_results = 25 if implicit_filter else 6

    needs_schema = where is not None or raw_filter is not None or implicit_filter

    resolved_schema = None
    if needs_schema:
        resolved_schema = _resolve_schema(
            config=config,
            provider=provider,
            schema_cache=schema_cache,
            knowledge_base_id=knowledge_base_id,
            metadata_schema_mode=metadata_schema_mode,
            metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
            metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
        )

    if raw_filter is not None:
        if not config.kb_allow_raw_filter:
            raise ValueError(
                'Raw filter passthrough is disabled. Set BEDROCK_KB_ALLOW_RAW_FILTER=true to enable.'
            )
        if resolved_schema is None:
            raise ValueError(
                'Raw filters require a resolved metadata schema. Provide a schema via env vars or enable auto mode.'
            )
        validation = validate_raw_filter_against_schema(
            schema=resolved_schema.schema,
            raw_filter=raw_filter,
        )
        if not validation.ok:
            raise ValueError(validation.error or 'Raw filter validation failed.')

    where_filter = None
    if resolved_schema is not None:
        try:
            where_filter = build_where_filter(
                schema=resolved_schema.schema,
                where=where,
                where_join=where_join,
            )
        except FilterError as e:
            raise ValueError(str(e)) from e

    explicit_filter = combine_filters_and([where_filter, raw_filter])

    implicit_filter_configuration = None
    if filter_mode in ('implicit_only', 'explicit_then_implicit') and implicit_filter:
        if resolved_schema is None:
            resolved_schema = _resolve_schema(
                config=config,
                provider=provider,
                schema_cache=schema_cache,
                knowledge_base_id=knowledge_base_id,
                metadata_schema_mode=metadata_schema_mode,
                metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
                metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
            )
        implicit_filter_configuration = _build_implicit_filter_configuration(
            config=config,
            schema=resolved_schema.schema,
        )

    retrieval_filter = None
    if filter_mode == 'explicit_only':
        retrieval_filter = explicit_filter
    elif filter_mode == 'implicit_only':
        retrieval_filter = None
    elif filter_mode == 'explicit_then_implicit':
        retrieval_filter = explicit_filter

    runtime_client, _agent_client = provider.get_clients()
    return await query_knowledge_base(
        query=query,
        knowledge_base_id=knowledge_base_id,
        kb_agent_client=runtime_client,
        number_of_results=effective_num_results,
        reranking=reranking,
        reranking_model_name=reranking_model_name,
        data_source_ids=data_source_ids,
        search_type=search_type,
        include_metadata=True,
        content_max_chars=content_max_chars,
        retrieval_filter=retrieval_filter,
        implicit_filter_configuration=implicit_filter_configuration,
    )
