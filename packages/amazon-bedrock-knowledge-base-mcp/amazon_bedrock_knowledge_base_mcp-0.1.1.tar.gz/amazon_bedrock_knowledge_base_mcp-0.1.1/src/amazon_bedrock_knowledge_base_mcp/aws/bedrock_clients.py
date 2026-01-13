# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65
"""Thin boto3 client constructors for Bedrock Knowledge Bases.

These helpers centralize how we create the Bedrock clients so other modules can stay focused on
retrieval logic and remain easy to test.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import boto3


if TYPE_CHECKING:
    from mypy_boto3_bedrock_agent.client import AgentsforBedrockClient
    from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
else:
    AgentsforBedrockClient = object
    AgentsforBedrockRuntimeClient = object


def get_bedrock_agent_runtime_client(
    region_name: str | None = None, profile_name: str | None = None
) -> AgentsforBedrockRuntimeClient:
    """Get a Bedrock agent runtime client.

    You access knowledge bases for RAG via the Bedrock agent runtime client.

    Args:
        region_name (str | None): The region name
        profile_name (str | None): The profile name
    """
    resolved_region = region_name or 'us-west-2'
    if profile_name:
        client = boto3.Session(profile_name=profile_name).client(
            'bedrock-agent-runtime', region_name=resolved_region
        )
        return client  # type: ignore
    client = boto3.client('bedrock-agent-runtime', region_name=resolved_region)
    return client  # type: ignore


def get_bedrock_agent_client(
    region_name: str | None = None, profile_name: str | None = None
) -> AgentsforBedrockClient:
    """Get a Bedrock agent management client.

    You access configuration and management of Knowledge Bases via the Bedrock agent client.

    Args:
        region_name (str | None): The region name
        profile_name (str | None): The profile name
    """
    resolved_region = region_name or 'us-west-2'
    if profile_name:
        client = boto3.Session(profile_name=profile_name).client(
            'bedrock-agent', region_name=resolved_region
        )
        return client  # type: ignore
    client = boto3.client('bedrock-agent', region_name=resolved_region)
    return client  # type: ignore
