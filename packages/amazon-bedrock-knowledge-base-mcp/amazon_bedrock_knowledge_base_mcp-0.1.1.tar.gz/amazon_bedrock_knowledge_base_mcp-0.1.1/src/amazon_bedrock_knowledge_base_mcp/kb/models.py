# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

"""Models and types for knowledge base discovery output."""

from __future__ import annotations

from typing import Dict, List, TypeAlias, TypedDict


class DataSource(TypedDict):
    """A data source for a knowledge base."""

    id: str
    name: str


class KnowledgeBase(TypedDict):
    """A knowledge base."""

    name: str
    description: str
    data_sources: List[DataSource]


KnowledgeBaseMapping: TypeAlias = Dict[str, KnowledgeBase]
