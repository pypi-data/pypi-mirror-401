# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Logging configuration utilities for the MCP server."""

from __future__ import annotations

import sys

from loguru import logger


_LOGGING_CONFIGURED = False


def configure_logging(*, level: str) -> None:
    """Configure loguru.

    This is intentionally opt-in (called from `main`) to avoid side effects at import time.
    """
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return
    logger.remove()
    logger.add(sys.stderr, level=level)
    _LOGGING_CONFIGURED = True
