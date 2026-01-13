# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Tests for AWS client initialization helpers."""

from __future__ import annotations

from amazon_bedrock_knowledge_base_mcp.aws import bedrock_clients as clients_module
from amazon_bedrock_knowledge_base_mcp.aws.bedrock_clients import (
    get_bedrock_agent_client,
    get_bedrock_agent_runtime_client,
)


class TestTypeDefinitions:
    """Tests for type definitions in clients.py."""

    def test_type_definitions(self):
        """Test that the type definitions are properly defined."""
        # Verify that the type aliases are defined
        assert hasattr(clients_module, 'AgentsforBedrockClient')
        assert hasattr(clients_module, 'AgentsforBedrockRuntimeClient')

        # Verify they are the expected types (object when not TYPE_CHECKING)
        assert clients_module.AgentsforBedrockClient is object
        assert clients_module.AgentsforBedrockRuntimeClient is object


class TestGetBedrockAgentRuntimeClient:
    """Tests for the get_bedrock_agent_runtime_client function."""

    def test_get_bedrock_agent_runtime_client_default(self, mock_boto3):
        """Test getting a Bedrock agent runtime client with default parameters."""
        client = get_bedrock_agent_runtime_client()

        # Check that boto3.client was called with the correct parameters
        mock_boto3['client'].assert_called_once_with(
            'bedrock-agent-runtime', region_name='us-west-2'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent_runtime']

    def test_get_bedrock_agent_runtime_client_with_region(self, mock_boto3):
        """Test getting a Bedrock agent runtime client with a specific region."""
        client = get_bedrock_agent_runtime_client(region_name='us-east-1')

        # Check that boto3.client was called with the correct parameters
        mock_boto3['client'].assert_called_once_with(
            'bedrock-agent-runtime', region_name='us-east-1'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent_runtime']

    def test_get_bedrock_agent_runtime_client_with_profile(self, mock_boto3):
        """Test getting a Bedrock agent runtime client with a specific profile."""
        client = get_bedrock_agent_runtime_client(profile_name='test-profile')

        # Check that boto3.Session was called with the correct parameters
        mock_boto3['Session'].assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct parameters
        mock_boto3['Session'].return_value.client.assert_called_once_with(
            'bedrock-agent-runtime', region_name='us-west-2'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent_runtime']

    def test_get_bedrock_agent_runtime_client_with_region_and_profile(self, mock_boto3):
        """Test getting a Bedrock agent runtime client with a specific region and profile."""
        client = get_bedrock_agent_runtime_client(
            region_name='us-east-1', profile_name='test-profile'
        )

        # Check that boto3.Session was called with the correct parameters
        mock_boto3['Session'].assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct parameters
        mock_boto3['Session'].return_value.client.assert_called_once_with(
            'bedrock-agent-runtime', region_name='us-east-1'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent_runtime']

    def test_get_bedrock_agent_runtime_client_with_none_region(self, mock_boto3):
        """Test getting a Bedrock agent runtime client with None region."""
        client = get_bedrock_agent_runtime_client(region_name=None)

        # Check that boto3.client was called with the correct parameters
        mock_boto3['client'].assert_called_once_with(
            'bedrock-agent-runtime', region_name='us-west-2'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent_runtime']


class TestGetBedrockAgentClient:
    """Tests for the get_bedrock_agent_client function."""

    def test_get_bedrock_agent_client_default(self, mock_boto3):
        """Test getting a Bedrock agent client with default parameters."""
        client = get_bedrock_agent_client()

        # Check that boto3.client was called with the correct parameters
        mock_boto3['client'].assert_called_once_with('bedrock-agent', region_name='us-west-2')

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent']

    def test_get_bedrock_agent_client_with_region(self, mock_boto3):
        """Test getting a Bedrock agent client with a specific region."""
        client = get_bedrock_agent_client(region_name='us-east-1')

        # Check that boto3.client was called with the correct parameters
        mock_boto3['client'].assert_called_once_with('bedrock-agent', region_name='us-east-1')

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent']

    def test_get_bedrock_agent_client_with_profile(self, mock_boto3):
        """Test getting a Bedrock agent client with a specific profile."""
        client = get_bedrock_agent_client(profile_name='test-profile')

        # Check that boto3.Session was called with the correct parameters
        mock_boto3['Session'].assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct parameters
        mock_boto3['Session'].return_value.client.assert_called_once_with(
            'bedrock-agent', region_name='us-west-2'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent']

    def test_get_bedrock_agent_client_with_region_and_profile(self, mock_boto3):
        """Test getting a Bedrock agent client with a specific region and profile."""
        client = get_bedrock_agent_client(region_name='us-east-1', profile_name='test-profile')

        # Check that boto3.Session was called with the correct parameters
        mock_boto3['Session'].assert_called_once_with(profile_name='test-profile')

        # Check that session.client was called with the correct parameters
        mock_boto3['Session'].return_value.client.assert_called_once_with(
            'bedrock-agent', region_name='us-east-1'
        )

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent']

    def test_get_bedrock_agent_client_with_none_region(self, mock_boto3):
        """Test getting a Bedrock agent client with None region."""
        client = get_bedrock_agent_client(region_name=None)

        # Check that boto3.client was called with the correct parameters
        mock_boto3['client'].assert_called_once_with('bedrock-agent', region_name='us-west-2')

        # Check that the client is the mock client
        assert client == mock_boto3['bedrock_agent']
