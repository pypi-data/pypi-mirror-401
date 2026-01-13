# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""FastMCP application factory.

This module creates and wires the FastMCP server without importing environment variables at import
time.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from loguru import logger
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import AnyHttpUrl, Field, TypeAdapter

from amazon_bedrock_knowledge_base_mcp.app.routes import register_health_routes
from amazon_bedrock_knowledge_base_mcp.app.service import (
    describe_metadata_schema,
    list_knowledge_bases,
    query_knowledge_bases,
    query_knowledge_bases_with_metadata,
)
from amazon_bedrock_knowledge_base_mcp.auth.auth0 import Auth0Config, Auth0JWTTokenVerifier
from amazon_bedrock_knowledge_base_mcp.aws.provider import DefaultBedrockClientsProvider
from amazon_bedrock_knowledge_base_mcp.core.config import (
    FilterMode,
    KnowledgeBaseSearchType,
    ServerConfig,
)
from amazon_bedrock_knowledge_base_mcp.kb.schema import (
    MetadataSchemaFile,
    SchemaMode,
    SchemaSource,
)


def _build_transport_security(config: ServerConfig) -> TransportSecuritySettings | None:
    if config.allowed_hosts_csv is None and config.allowed_origins_csv is None:
        return None

    if (config.allowed_hosts_csv in ('', '*')) or (config.allowed_origins_csv in ('', '*')):
        logger.warning(
            'Transport security: DNS rebinding protection is disabled '
            '(MCP_ALLOWED_HOSTS / MCP_ALLOWED_ORIGINS is empty or "*").'
        )
        return TransportSecuritySettings(enable_dns_rebinding_protection=False)

    allowed_hosts = []
    if config.allowed_hosts_csv:
        allowed_hosts = [h.strip() for h in config.allowed_hosts_csv.split(',') if h.strip()]

    allowed_origins = []
    if config.allowed_origins_csv:
        allowed_origins = [o.strip() for o in config.allowed_origins_csv.split(',') if o.strip()]

    if allowed_hosts and allowed_origins:
        return TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=allowed_hosts,
            allowed_origins=allowed_origins,
        )
    return TransportSecuritySettings(enable_dns_rebinding_protection=False)


def create_mcp_server(*, config: ServerConfig) -> FastMCP:
    """Create a configured FastMCP server instance."""
    auth_settings = None
    token_verifier = None
    if config.auth_mode == 'oauth':
        assert config.auth0_domain is not None
        assert config.auth0_audience is not None
        assert config.mcp_resource_url is not None

        issuer_url = TypeAdapter(AnyHttpUrl).validate_python(f'https://{config.auth0_domain}')
        resource_server_url = TypeAdapter(AnyHttpUrl).validate_python(config.mcp_resource_url)

        auth_settings = AuthSettings(
            issuer_url=issuer_url,
            resource_server_url=resource_server_url,
            required_scopes=None,
        )
        token_verifier = Auth0JWTTokenVerifier(
            config=Auth0Config(domain=config.auth0_domain, audience=config.auth0_audience)
        )

    provider = DefaultBedrockClientsProvider(config=config)
    schema_cache: dict[str, tuple[MetadataSchemaFile, SchemaSource]] = {}

    mcp = FastMCP(
        'amazon-bedrock-knowledge-base-mcp',
        instructions=(
            'Retrieve information from Amazon Bedrock Knowledge Bases.\n'
            '\n'
            'Recommended workflow:\n'
            '1) Call ListKnowledgeBases to find an eligible knowledge base and its data sources.\n'
            '2) Use QueryKnowledgeBases for content-focused retrieval.\n'
            '3) Use QueryKnowledgeBasesWithMetadata for discovery and metadata-aware exploration.\n'
            '4) If you want filtering, call DescribeMetadataSchema first, then use `where` (friendly) or '
            '`filter` (raw) constraints.\n'
            '\n'
            'Prefer small `number_of_results` for focused answers, and enable reranking when you need better '
            'ordering.'
        ),
        dependencies=['boto3'],
        host=config.host,
        port=config.port,
        streamable_http_path='/mcp',
        stateless_http=config.stateless_http,
        json_response=config.json_response,
        auth=auth_settings,
        token_verifier=token_verifier,
        transport_security=_build_transport_security(config),
        log_level=config.log_level,  # type: ignore[arg-type]
    )

    register_health_routes(mcp, config=config)

    @mcp.tool(name='DescribeMetadataSchema')
    async def describe_metadata_schema_tool(
        knowledge_base_id: Annotated[
            str,
            Field(
                description=(
                    'The knowledge base ID to inspect. It must be a valid ID from the ListKnowledgeBases tool.'
                )
            ),
        ],
        metadata_schema_mode: Annotated[
            SchemaMode,
            Field(
                description=(
                    "Metadata schema resolution mode. 'static' uses only configured schema files; 'auto' "
                    'falls back to sampling retrieval metadata to infer a schema.'
                )
            ),
        ] = 'auto',
        metadata_schema_auto_sample_query: Annotated[
            str,
            Field(
                description='Query used for auto schema discovery (only when metadata_schema_mode=auto).'
            ),
        ] = 'the',
        metadata_schema_auto_sample_k: Annotated[
            int,
            Field(description='Number of retrieval results to sample for auto schema discovery.'),
        ] = 10,
    ) -> str:
        """Describe the metadata schema used for filtering.

        Returns a JSON string describing the effective schema for a knowledge base. Use this before
        applying metadata filters via `where`, `filter`, or implicit filtering.
        """
        return await describe_metadata_schema(
            config=config,
            provider=provider,
            schema_cache=schema_cache,
            knowledge_base_id=knowledge_base_id,
            metadata_schema_mode=metadata_schema_mode,
            metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
            metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
        )

    @mcp.tool(name='ListKnowledgeBases')
    async def list_knowledge_bases_tool() -> str:
        """List available knowledge bases and their data sources.

        Returns a JSON string mapping knowledge base IDs to `{name, description, data_sources}`.
        """
        return await list_knowledge_bases(config=config, provider=provider)

    @mcp.tool(name='QueryKnowledgeBases')
    async def query_knowledge_bases_tool(
        query: Annotated[
            str, Field(description='A natural language query to search the knowledge base with')
        ],
        knowledge_base_id: Annotated[
            str,
            Field(
                description=(
                    'The knowledge base ID to query. It must be a valid ID from the ListKnowledgeBases tool.'
                )
            ),
        ],
        number_of_results: Annotated[
            int,
            Field(
                description=(
                    'The number of results to return. Use smaller values for focused results and larger values '
                    'for broader coverage.'
                )
            ),
        ] = 10,
        reranking: Annotated[
            bool,
            Field(
                description=(
                    'Whether to rerank the results. Useful for improving relevance and sorting. '
                    'Can be globally configured with BEDROCK_KB_RERANKING_ENABLED.'
                )
            ),
        ] = config.kb_reranking_enabled,
        reranking_model_name: Annotated[
            Literal['COHERE', 'AMAZON'],
            Field(
                description="The name of the reranking model to use. Options: 'COHERE', 'AMAZON'."
            ),
        ] = 'AMAZON',
        data_source_ids: Annotated[
            list[str] | None,
            Field(
                description=(
                    'The data source IDs to filter the knowledge base by. It must be a list of valid data source '
                    'IDs from the ListKnowledgeBases tool.'
                )
            ),
        ] = None,
        filter_mode: Annotated[
            FilterMode,
            Field(
                description=(
                    'How to combine explicit filters (`where`/raw) and implicit filtering. '
                    "'explicit_then_implicit' applies explicit filters when provided, and also enables implicit "
                    'filtering when requested; it composes constraints with AND semantics.'
                )
            ),
        ] = config.kb_filter_mode,
        where_join: Annotated[
            Literal['AND', 'OR'],
            Field(
                description=(
                    'How to combine schema-driven `where` constraints. Default is AND (narrow). '
                    'OR is supported within friendly filters only.'
                )
            ),
        ] = 'AND',
        where: Annotated[
            dict[str, Any] | None,
            Field(
                description=(
                    'Optional schema-driven metadata constraints. Keys are resolved via the metadata schema: '
                    'prefer schema aliases, or use direct metadata keys. Values can be scalars, lists (OR within '
                    'that key), or dicts for operator overrides.'
                )
            ),
        ] = None,
        filter: Annotated[
            dict[str, Any] | None,
            Field(
                description=(
                    'Optional raw Bedrock retrieval filter (RetrievalFilter). '
                    'This is a power-user escape hatch and is only accepted when BEDROCK_KB_ALLOW_RAW_FILTER=true.'
                )
            ),
        ] = None,  # noqa: A002
        implicit_filter: Annotated[
            bool,
            Field(
                description=(
                    'Enable Bedrock implicit filtering for this call (requires BEDROCK_KB_IMPLICIT_FILTER_MODEL_ARN).'
                )
            ),
        ] = False,
        metadata_schema_mode: Annotated[
            SchemaMode,
            Field(
                description=(
                    "Metadata schema resolution mode. 'static' uses only configured schema files; 'auto' "
                    'falls back to sampling retrieval metadata to infer a schema.'
                )
            ),
        ] = 'auto',
        metadata_schema_auto_sample_query: Annotated[
            str,
            Field(
                description='Query used for auto schema discovery (only when metadata_schema_mode=auto).'
            ),
        ] = 'the',
        metadata_schema_auto_sample_k: Annotated[
            int,
            Field(description='Number of retrieval results to sample for auto schema discovery.'),
        ] = 10,
        search_type: Annotated[
            KnowledgeBaseSearchType,
            Field(
                description=(
                    "Search strategy for retrieval. 'HYBRID' combines keyword + semantic search and is recommended "
                    "for OpenSearch Serverless; 'SEMANTIC' uses embeddings only; 'DEFAULT' lets Bedrock decide."
                )
            ),
        ] = config.kb_search_type,
    ) -> str:
        """Query a knowledge base and return relevant passages.

        Returns a newline-separated set of JSON objects (one per retrieval result).
        """
        return await query_knowledge_bases(
            config=config,
            provider=provider,
            schema_cache=schema_cache,
            query=query,
            knowledge_base_id=knowledge_base_id,
            number_of_results=number_of_results,
            reranking=reranking,
            reranking_model_name=reranking_model_name,
            data_source_ids=data_source_ids,
            search_type=search_type,
            filter_mode=filter_mode,
            where_join=where_join,
            where=where,
            raw_filter=filter,
            implicit_filter=implicit_filter,
            metadata_schema_mode=metadata_schema_mode,
            metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
            metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
        )

    @mcp.tool(name='QueryKnowledgeBasesWithMetadata')
    async def query_knowledge_bases_with_metadata_tool(
        query: Annotated[
            str, Field(description='A natural language query to search the knowledge base with')
        ],
        knowledge_base_id: Annotated[
            str,
            Field(
                description=(
                    'The knowledge base ID to query. It must be a valid ID from the ListKnowledgeBases tool.'
                )
            ),
        ],
        number_of_results: Annotated[
            int | None,
            Field(
                description=(
                    'The number of results to return. Prefer smaller values for metadata-driven discovery. '
                    'If omitted and implicit_filter=true, defaults to 25; otherwise defaults to 6.'
                )
            ),
        ] = None,
        reranking: Annotated[
            bool,
            Field(
                description=(
                    'Whether to rerank the results. Useful for improving relevance and sorting. '
                    'Can be globally configured with BEDROCK_KB_RERANKING_ENABLED.'
                )
            ),
        ] = config.kb_reranking_enabled,
        reranking_model_name: Annotated[
            Literal['COHERE', 'AMAZON'],
            Field(
                description="The name of the reranking model to use. Options: 'COHERE', 'AMAZON'."
            ),
        ] = 'AMAZON',
        data_source_ids: Annotated[
            list[str] | None,
            Field(
                description=(
                    'The data source IDs to filter the knowledge base by. It must be a list of valid data source '
                    'IDs from the ListKnowledgeBases tool.'
                )
            ),
        ] = None,
        content_max_chars: Annotated[
            int | None,
            Field(
                description=(
                    'If set, truncate returned TEXT content to this many characters to reduce tool output size.'
                )
            ),
        ] = 600,
        filter_mode: Annotated[
            FilterMode,
            Field(
                description=(
                    'How to combine explicit filters (`where`/raw) and implicit filtering. '
                    "'explicit_then_implicit' applies explicit filters when provided, and also enables implicit "
                    'filtering when requested; it composes constraints with AND semantics.'
                )
            ),
        ] = config.kb_filter_mode,
        where_join: Annotated[
            Literal['AND', 'OR'],
            Field(
                description=(
                    'How to combine schema-driven `where` constraints. Default is AND (narrow). '
                    'OR is supported within friendly filters only.'
                )
            ),
        ] = 'AND',
        where: Annotated[
            dict[str, Any] | None,
            Field(
                description=(
                    'Optional schema-driven metadata constraints. Keys are resolved via the metadata schema: '
                    'prefer schema aliases, or use direct metadata keys. Values can be scalars, lists (OR within '
                    'that key), or dicts for operator overrides.'
                )
            ),
        ] = None,
        filter: Annotated[
            dict[str, Any] | None,
            Field(
                description=(
                    'Optional raw Bedrock retrieval filter (RetrievalFilter). '
                    'This is a power-user escape hatch and is only accepted when BEDROCK_KB_ALLOW_RAW_FILTER=true.'
                )
            ),
        ] = None,  # noqa: A002
        implicit_filter: Annotated[
            bool,
            Field(
                description=(
                    'Enable Bedrock implicit filtering for this call (requires BEDROCK_KB_IMPLICIT_FILTER_MODEL_ARN).'
                )
            ),
        ] = False,
        metadata_schema_mode: Annotated[
            SchemaMode,
            Field(
                description=(
                    "Metadata schema resolution mode. 'static' uses only configured schema files; 'auto' "
                    'falls back to sampling retrieval metadata to infer a schema.'
                )
            ),
        ] = 'auto',
        metadata_schema_auto_sample_query: Annotated[
            str,
            Field(
                description='Query used for auto schema discovery (only when metadata_schema_mode=auto).'
            ),
        ] = 'the',
        metadata_schema_auto_sample_k: Annotated[
            int,
            Field(description='Number of retrieval results to sample for auto schema discovery.'),
        ] = 10,
        search_type: Annotated[
            KnowledgeBaseSearchType,
            Field(
                description=(
                    "Search strategy for retrieval. 'HYBRID' combines keyword + semantic search and is recommended "
                    "for OpenSearch Serverless; 'SEMANTIC' uses embeddings only; 'DEFAULT' lets Bedrock decide."
                )
            ),
        ] = config.kb_search_type,
    ) -> str:
        """Query a knowledge base and include metadata in results.

        Use this for metadata-driven exploration (discover what keys/values exist) before applying
        precise filters. Returns newline-separated JSON objects.
        """
        return await query_knowledge_bases_with_metadata(
            config=config,
            provider=provider,
            schema_cache=schema_cache,
            query=query,
            knowledge_base_id=knowledge_base_id,
            number_of_results=number_of_results,
            reranking=reranking,
            reranking_model_name=reranking_model_name,
            data_source_ids=data_source_ids,
            content_max_chars=content_max_chars,
            search_type=search_type,
            filter_mode=filter_mode,
            where_join=where_join,
            where=where,
            raw_filter=filter,
            implicit_filter=implicit_filter,
            metadata_schema_mode=metadata_schema_mode,
            metadata_schema_auto_sample_query=metadata_schema_auto_sample_query,
            metadata_schema_auto_sample_k=metadata_schema_auto_sample_k,
        )

    logger.debug(
        'Registered MCP tools: DescribeMetadataSchema, ListKnowledgeBases, QueryKnowledgeBases, QueryKnowledgeBasesWithMetadata'
    )

    return mcp
