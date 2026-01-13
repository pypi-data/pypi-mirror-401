# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Amazon Bedrock Knowledge Base Retrieval MCP Server (standalone)."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as _dist_version

__version__ = '0.1.0'

# Prefer distribution metadata when installed from a wheel/sdist, while keeping a static fallback
# for editable/dev checkouts and semantic-release version bumping.
try:
    __version__ = _dist_version('amazon-bedrock-knowledge-base-mcp')
except PackageNotFoundError:
    pass
except Exception:
    pass
