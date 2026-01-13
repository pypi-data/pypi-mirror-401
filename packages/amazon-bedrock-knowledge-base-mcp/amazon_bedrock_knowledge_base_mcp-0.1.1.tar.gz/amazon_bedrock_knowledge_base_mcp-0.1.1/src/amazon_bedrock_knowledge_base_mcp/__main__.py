# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Module entrypoint for `python -m amazon_bedrock_knowledge_base_mcp`.

Docs recommend running via `uv`, but this provides a standard Python execution path.
"""

from __future__ import annotations

from amazon_bedrock_knowledge_base_mcp.server import main


if __name__ == '__main__':
    main()
