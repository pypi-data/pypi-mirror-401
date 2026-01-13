# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Literal

from loguru import logger


if TYPE_CHECKING:
    from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from mypy_boto3_bedrock_agent_runtime.type_defs import (
        KnowledgeBaseRetrievalConfigurationTypeDef,
    )
else:
    AgentsforBedrockRuntimeClient = object
    KnowledgeBaseRetrievalConfigurationTypeDef = object


async def query_knowledge_base(
    query: str,
    knowledge_base_id: str,
    kb_agent_client: AgentsforBedrockRuntimeClient,
    number_of_results: int = 20,
    reranking: bool = False,
    reranking_model_name: Literal['COHERE', 'AMAZON'] = 'AMAZON',
    data_source_ids: list[str] | None = None,
    search_type: Literal['HYBRID', 'SEMANTIC', 'DEFAULT'] = 'DEFAULT',
    include_metadata: bool = False,
    content_max_chars: int | None = None,
    retrieval_filter: dict[str, Any] | None = None,
    implicit_filter_configuration: dict[str, Any] | None = None,
) -> str:
    """Query an Amazon Bedrock Knowledge Base.

    Args:
        query: Natural language query text.
        knowledge_base_id: Bedrock knowledge base ID.
        kb_agent_client: Bedrock Agent Runtime client.
        number_of_results: Max number of results.
        reranking: Whether to enable reranking.
        reranking_model_name: Reranking provider selection.
        data_source_ids: Optional list of data source IDs to scope retrieval.
        search_type: Retrieval strategy override (`HYBRID`, `SEMANTIC`, or `DEFAULT`).
        include_metadata: Include Bedrock metadata for each result.
        content_max_chars: If set, truncate TEXT content to this many characters.
        retrieval_filter: Optional Bedrock RetrievalFilter to apply (AND-composed with `data_source_ids`).
        implicit_filter_configuration: Optional Bedrock implicit filtering configuration.

    Returns:
        Newline-separated JSON documents (one per retrieval result).

    Raises:
        ValueError: If reranking is requested in an unsupported region.
    """
    if reranking and kb_agent_client.meta.region_name not in [
        'us-west-2',
        'us-east-1',
        'ap-northeast-1',
        'ca-central-1',
        'eu-central-1',
    ]:
        raise ValueError(
            f'Reranking is not supported in region {kb_agent_client.meta.region_name}'
        )

    retrieve_request: KnowledgeBaseRetrievalConfigurationTypeDef = {
        'vectorSearchConfiguration': {
            'numberOfResults': number_of_results,
        }
    }

    if search_type in ('HYBRID', 'SEMANTIC'):
        retrieve_request['vectorSearchConfiguration']['overrideSearchType'] = search_type  # type: ignore

    filters: list[dict[str, Any]] = []
    if data_source_ids:
        filters.append(
            {
                'in': {
                    'key': 'x-amz-bedrock-kb-data-source-id',
                    'value': data_source_ids,  # type: ignore
                }
            }
        )
    if retrieval_filter:
        filters.append(retrieval_filter)

    if filters:
        if len(filters) == 1:
            retrieve_request['vectorSearchConfiguration']['filter'] = filters[0]  # type: ignore
        else:
            retrieve_request['vectorSearchConfiguration']['filter'] = {'andAll': filters}  # type: ignore

    if implicit_filter_configuration:
        retrieve_request['vectorSearchConfiguration']['implicitFilterConfiguration'] = (  # type: ignore
            implicit_filter_configuration
        )

    if reranking:
        model_name_mapping = {
            'COHERE': 'cohere.rerank-v3-5:0',
            'AMAZON': 'amazon.rerank-v1:0',
        }
        retrieve_request['vectorSearchConfiguration']['rerankingConfiguration'] = {
            'type': 'BEDROCK_RERANKING_MODEL',
            'bedrockRerankingConfiguration': {
                'modelConfiguration': {
                    'modelArn': f'arn:aws:bedrock:{kb_agent_client.meta.region_name}::foundation-model/{model_name_mapping[reranking_model_name]}'
                },
            },
        }

    response = kb_agent_client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={'text': query},
        retrievalConfiguration=retrieve_request,
    )
    results = response['retrievalResults']
    documents: list[dict] = []
    for result in results:
        if result['content'].get('type') == 'IMAGE':
            logger.warning('Images are not supported at this time. Skipping...')
            continue
        content = result['content']
        if content_max_chars and isinstance(content, dict) and content.get('type') == 'TEXT':
            text = content.get('text') or ''
            if isinstance(text, str) and len(text) > content_max_chars:
                content = {**content, 'text': text[:content_max_chars] + '…'}

        document = {
            'content': content,
            'location': result.get('location', ''),
            'score': result.get('score', ''),
        }
        if include_metadata:
            document['metadata'] = result.get('metadata', {})
        documents.append(document)

    return '\n\n'.join([json.dumps(document) for document in documents])
