# Schemas

This folder contains example metadata schema files used for:

- translating friendly `where` filters into Bedrock RetrievalFilter expressions
- validating raw `filter` passthrough when `BEDROCK_KB_ALLOW_RAW_FILTER=true`
- providing metadata attributes to Bedrock implicit filtering (`implicit_filter=true`)

## Examples

- `examples/metadata-schema.example.json`: a single schema file
- `examples/metadata-schema-map.local.example.json`: KB ID → schema file path map (local dev)
- `examples/metadata-schema-map.container.example.json`: KB ID → schema file path map (container deployments)

## Environment variables

- `BEDROCK_KB_SCHEMA_MAP_JSON=/absolute/path/to/schema-map.json`
- `BEDROCK_KB_SCHEMA_DEFAULT_PATH=/absolute/path/to/default.schema.json`
