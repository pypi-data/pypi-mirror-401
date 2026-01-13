# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Tests for the models module."""

from amazon_bedrock_knowledge_base_mcp.kb.models import (
    DataSource,
    KnowledgeBase,
    KnowledgeBaseMapping,
)


class TestDataSource:
    """Tests for the DataSource model."""

    def test_data_source_creation(self):
        """Test creating a DataSource."""
        data_source = DataSource(id='ds-12345', name='Test Data Source')

        assert data_source['id'] == 'ds-12345'
        assert data_source['name'] == 'Test Data Source'


class TestKnowledgeBase:
    """Tests for the KnowledgeBase model."""

    def test_knowledge_base_creation(self):
        """Test creating a KnowledgeBase."""
        data_sources = [
            DataSource(id='ds-12345', name='Test Data Source'),
            DataSource(id='ds-67890', name='Another Data Source'),
        ]

        knowledge_base = KnowledgeBase(
            name='Test Knowledge Base',
            description='A test knowledge base',
            data_sources=data_sources,
        )

        assert knowledge_base['name'] == 'Test Knowledge Base'
        assert knowledge_base['description'] == 'A test knowledge base'
        assert len(knowledge_base['data_sources']) == 2
        assert knowledge_base['data_sources'][0]['id'] == 'ds-12345'
        assert knowledge_base['data_sources'][0]['name'] == 'Test Data Source'
        assert knowledge_base['data_sources'][1]['id'] == 'ds-67890'
        assert knowledge_base['data_sources'][1]['name'] == 'Another Data Source'


class TestKnowledgeBaseMapping:
    """Tests for the KnowledgeBaseMapping type."""

    def test_knowledge_base_mapping(self):
        """Test creating a KnowledgeBaseMapping."""
        data_sources1 = [DataSource(id='ds-12345', name='Test Data Source')]
        data_sources2 = [DataSource(id='ds-67890', name='Another Data Source')]

        kb1 = KnowledgeBase(
            name='Test Knowledge Base',
            description='First test knowledge base',
            data_sources=data_sources1,
        )
        kb2 = KnowledgeBase(
            name='Another Knowledge Base',
            description='Second test knowledge base',
            data_sources=data_sources2,
        )

        kb_mapping: KnowledgeBaseMapping = {'kb-12345': kb1, 'kb-67890': kb2}

        assert len(kb_mapping) == 2
        assert kb_mapping['kb-12345']['name'] == 'Test Knowledge Base'
        assert kb_mapping['kb-12345']['description'] == 'First test knowledge base'
        assert kb_mapping['kb-67890']['name'] == 'Another Knowledge Base'
        assert kb_mapping['kb-67890']['description'] == 'Second test knowledge base'
        assert kb_mapping['kb-12345']['data_sources'][0]['id'] == 'ds-12345'
        assert kb_mapping['kb-67890']['data_sources'][0]['id'] == 'ds-67890'
