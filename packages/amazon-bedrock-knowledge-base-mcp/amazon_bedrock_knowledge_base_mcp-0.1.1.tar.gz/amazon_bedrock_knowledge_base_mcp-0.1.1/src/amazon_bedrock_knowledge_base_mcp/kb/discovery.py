# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

from typing import TYPE_CHECKING

from loguru import logger

from .models import KnowledgeBaseMapping


if TYPE_CHECKING:
    from mypy_boto3_bedrock_agent import AgentsforBedrockClient
else:
    AgentsforBedrockClient = object


DEFAULT_KNOWLEDGE_BASE_TAG_INCLUSION_KEY = 'mcp-multirag-kb'


async def discover_knowledge_bases(
    agent_client: AgentsforBedrockClient,
    tag_key: str = DEFAULT_KNOWLEDGE_BASE_TAG_INCLUSION_KEY,
) -> KnowledgeBaseMapping:
    """Discover knowledge bases.

    Args:
        agent_client (AgentsforBedrockClient): The Bedrock agent client
        tag_key (str): The tag key to filter knowledge bases by

    Returns:
        KnowledgeBaseMapping: A mapping of knowledge base IDs to knowledge base details
    """
    result: KnowledgeBaseMapping = {}

    kb_data = []
    kb_paginator = agent_client.get_paginator('list_knowledge_bases')

    for page in kb_paginator.paginate():
        for kb in page.get('knowledgeBaseSummaries', []):
            logger.debug(f'KB: {kb}')
            kb_id = kb.get('knowledgeBaseId')
            kb_name = kb.get('name')
            kb_description = kb.get('description', '')

            kb_arn = (
                agent_client.get_knowledge_base(knowledgeBaseId=kb_id)
                .get('knowledgeBase', {})
                .get('knowledgeBaseArn')
            )

            tags = agent_client.list_tags_for_resource(resourceArn=kb_arn).get('tags', {})
            if tag_key in tags and tags[tag_key] == 'true':
                logger.debug(f'KB Name: {kb_name}')
                kb_data.append((kb_id, kb_name, kb_description))

    for kb_id, kb_name, kb_description in kb_data:
        result[kb_id] = {'name': kb_name, 'description': kb_description, 'data_sources': []}

        data_sources = []
        data_sources_paginator = agent_client.get_paginator('list_data_sources')

        for page in data_sources_paginator.paginate(knowledgeBaseId=kb_id):
            for ds in page.get('dataSourceSummaries', []):
                ds_id = ds.get('dataSourceId')
                ds_name = ds.get('name')
                logger.debug(f'DS: {ds}')
                data_sources.append({'id': ds_id, 'name': ds_name})

        result[kb_id]['data_sources'] = data_sources

    return result
