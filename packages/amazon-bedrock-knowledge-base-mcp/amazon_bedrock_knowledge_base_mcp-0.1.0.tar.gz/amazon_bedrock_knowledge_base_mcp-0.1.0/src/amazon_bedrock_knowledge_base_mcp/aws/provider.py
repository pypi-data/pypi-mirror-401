# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Bedrock client provider with lazy initialization.

This avoids constructing boto3 clients at import time and keeps them cached for reuse.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

from loguru import logger

from amazon_bedrock_knowledge_base_mcp.aws.bedrock_clients import (
    get_bedrock_agent_client,
    get_bedrock_agent_runtime_client,
)
from amazon_bedrock_knowledge_base_mcp.core.config import ServerConfig


if TYPE_CHECKING:
    from mypy_boto3_bedrock_agent.client import AgentsforBedrockClient
    from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
else:
    AgentsforBedrockClient = object
    AgentsforBedrockRuntimeClient = object


class BedrockClientsProvider(Protocol):
    """Protocol for providing Bedrock clients."""

    def get_clients(self) -> tuple[AgentsforBedrockRuntimeClient, AgentsforBedrockClient]:
        """Return (runtime_client, agent_management_client)."""
        ...


@dataclass(slots=True)
class DefaultBedrockClientsProvider:
    """Default cached Bedrock client provider."""

    config: ServerConfig
    _runtime_client: Any = None
    _agent_mgmt_client: Any = None

    def get_clients(self) -> tuple[AgentsforBedrockRuntimeClient, AgentsforBedrockClient]:
        """Create or return cached Bedrock clients.

        Returns:
            tuple[AgentsforBedrockRuntimeClient, AgentsforBedrockClient]: `(runtime, agent_management)`.
        """
        if self._runtime_client is not None and self._agent_mgmt_client is not None:
            return (self._runtime_client, self._agent_mgmt_client)

        try:
            self._runtime_client = get_bedrock_agent_runtime_client(
                region_name=self.config.aws_region,
                profile_name=self.config.aws_profile,
            )
            self._agent_mgmt_client = get_bedrock_agent_client(
                region_name=self.config.aws_region,
                profile_name=self.config.aws_profile,
            )
        except Exception as e:
            logger.error(f'Error getting bedrock agent clients: {e}')
            raise

        return (self._runtime_client, self._agent_mgmt_client)
