# STDIO Setup Guide

This guide covers setting up the Amazon Bedrock Knowledge Base MCP server in STDIO mode for Claude Desktop and local development.

---

## Claude Desktop

Download: https://claude.com/download (install guide: https://support.claude.com/en/articles/10065433-installing-claude-for-desktop)

### Configuration File Location

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%/Claude/claude_desktop_config.json` |

> **Tip:** In Claude Desktop, go to **Settings > Developer > Edit Config** to open the file directly.

### Basic Configuration

```json
{
  "mcpServers": {
    "amazon-bedrock-kb": {
      "command": "uvx",
      "args": ["amazon-bedrock-knowledge-base-mcp"],
      "env": {
        "AWS_PROFILE": "your-profile-name",
        "AWS_REGION": "us-west-2"
      }
    }
  }
}
```

---

### Filtering schema configuration (optional but recommended)

To use schema-driven filtering, configure schema paths.

```json
{
  "env": {
    "BEDROCK_KB_ALLOW_RAW_FILTER": "false",
    "BEDROCK_KB_FILTER_MODE": "explicit_then_implicit",
    "BEDROCK_KB_SCHEMA_MAP_JSON": "/absolute/path/to/schemas/metadata-schema-map.json"
  }
}
```

### Reranking and search type defaults (optional)

```json
{
  "env": {
    "BEDROCK_KB_RERANKING_ENABLED": "false",
    "BEDROCK_KB_SEARCH_TYPE": "HYBRID"
  }
}
```

---

## Local Development

### Prerequisites

- Python 3.10+
- `uv` / `uvx` installed: [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- AWS credentials with access to Amazon Bedrock Knowledge Bases (see
  [Knowledge Bases for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
- Recommended: IAM role on EC2 (see
  [IAM roles for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html))
- If you use `AWS_PROFILE`, configure it via the standard AWS shared config/credentials files (see
  [AWS CLI configuration files](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html))

### Clone and Install

```bash
git clone https://github.com/Zlash65/amazon-bedrock-knowledge-base-mcp.git

cd amazon-bedrock-knowledge-base-mcp
uv sync
```

### Run from Source

```bash
# Set environment variables
export AWS_PROFILE="your-profile-name"
export AWS_REGION="us-west-2"

# Run the STDIO server
uv run amazon-bedrock-knowledge-base-mcp
```

### Connect Claude Desktop to Local Build

Point Claude Desktop to your local repo instead of `uvx`:

```json
{
  "mcpServers": {
    "amazon-bedrock-kb-dev": {
      "command": "uv",
      "args": [
        "--project",
        "/absolute/path/to/amazon-bedrock-knowledge-base-mcp",
        "run",
        "amazon-bedrock-knowledge-base-mcp"
      ],
      "env": {
        "AWS_PROFILE": "your-profile-name",
        "AWS_REGION": "us-west-2"
      }
    }
  }
}
```

### Development Workflow

```bash
# Watch mode for Python (re-run on changes)
uv run --with watchfiles watchfiles "uv run pytest -q"

# Run tests
uv run pytest -q

# Run tests in watch mode
uv run --with pytest-watch ptw --runner "uv run pytest -q"

# Type check
uv run pyright

# Lint
uv run ruff check .
```

---

### Test AWS Credentials with Docker

If you want a quick sanity check for your host AWS profile:

```bash
docker run --rm \
  -v "$HOME/.aws:/root/.aws:ro" \
  -e AWS_PROFILE=your-profile-name \
  amazon/aws-cli sts get-caller-identity
```

---

## Other MCP Clients

Any MCP client that launches commands with environment variables can use:

```
command: uvx
args: ["amazon-bedrock-knowledge-base-mcp"]
```

Or, if you install the package in a venv:

```
command: /path/to/venv/bin/amazon-bedrock-knowledge-base-mcp
args: []
```

---

## Notes

- `ListKnowledgeBases` only includes knowledge bases tagged with `<KB_INCLUSION_TAG_KEY>=true` (default key: `mcp-multirag-kb`).
- Prefer `AWS_PROFILE` + `AWS_REGION` over long-lived credentials.
- Use `DescribeMetadataSchema` to confirm which metadata keys are available for filtering.
