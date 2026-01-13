# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

import pytest
from pydantic import ValidationError

from amazon_bedrock_knowledge_base_mcp.kb.schema import (
    ImplicitFilterSchemaConfig,
    MetadataFieldSchema,
    MetadataSchemaFile,
    schema_to_implicit_metadata_attributes,
)


def _mk_schema(keys: list[str]) -> MetadataSchemaFile:
    return MetadataSchemaFile(metadata={k: MetadataFieldSchema(type='STRING') for k in keys})


def test_implicit_filter_enforces_max_25_when_unconfigured():
    """Reject schemas with >25 implicit metadata keys when no subset is configured."""
    schema = _mk_schema([f'k{i}' for i in range(26)])
    with pytest.raises(ValueError, match='at most 25'):
        schema_to_implicit_metadata_attributes(schema)


def test_implicit_filter_include_keys_selects_subset_and_preserves_order():
    """Use include_keys exactly (order preserved) and enforce <=25."""
    all_keys = [f'k{i}' for i in range(30)]
    include = [f'k{i}' for i in range(25)]
    schema = MetadataSchemaFile(
        metadata={k: MetadataFieldSchema(type='STRING') for k in all_keys},
        implicit_filter=ImplicitFilterSchemaConfig(include_keys=include),
    )
    attrs = schema_to_implicit_metadata_attributes(schema)
    assert [a['key'] for a in attrs] == include
    assert len(attrs) == 25


def test_implicit_filter_include_keys_rejects_unknown_keys():
    """Reject include_keys values that are not present in schema.metadata."""
    schema = MetadataSchemaFile(
        metadata={'known': MetadataFieldSchema(type='STRING')},
        implicit_filter=ImplicitFilterSchemaConfig(include_keys=['known', 'unknown']),
    )
    with pytest.raises(ValueError, match='unknown metadata keys'):
        schema_to_implicit_metadata_attributes(schema)


def test_implicit_filter_rejects_include_and_exclude_together():
    """Reject schemas that set both include_keys and exclude_keys."""
    with pytest.raises(ValidationError, match='both include_keys and exclude_keys'):
        MetadataSchemaFile(
            metadata={'k': MetadataFieldSchema(type='STRING')},
            implicit_filter=ImplicitFilterSchemaConfig(include_keys=['k'], exclude_keys=['k']),
        )
