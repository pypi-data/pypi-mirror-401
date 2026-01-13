# Streamable HTTP Setup Guide

This guide covers setting up the Amazon Bedrock Knowledge Base MCP server in HTTP mode for ChatGPT, web clients, and local development.

---

## Quick Start

Prereqs:

- `uv` / `uvx` installed: [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- AWS credentials with access to Amazon Bedrock Knowledge Bases:
  [Knowledge Bases for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)

```bash
AWS_REGION="us-west-2" \
MCP_TRANSPORT="streamable-http" \
MCP_HOST="0.0.0.0" \
PORT="8000" \
MCP_STATELESS="true" \
  uvx amazon-bedrock-knowledge-base-mcp
```

The MCP endpoint is available at `http://localhost:8000/mcp`.

If you're setting this up for ChatGPT, see [ChatGPT Setup Guide](chatgpt-setup.md) and open
[chatgpt.com](https://chatgpt.com/).

---

## Configuration

### Basic Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | Must be `streamable-http` for remote HTTP |
| `PORT` | `8000` | HTTP server port |
| `MCP_HOST` | `127.0.0.1` | Bind address |
| `MCP_STATELESS` | `true` | Stateless mode (recommended for ChatGPT) |
| `MCP_AUTH_MODE` | `none` | `none` or `oauth` |

### Stateless vs Stateful Mode

**Stateless (`MCP_STATELESS=true`, default):**
- Each request includes the MCP initialize handshake
- Only `POST /mcp` is available
- No session storage between requests
- Recommended for ChatGPT and serverless deployments

**Stateful (`MCP_STATELESS=false`):**
- Clients maintain a session ID across requests
- `POST /mcp`, `GET /mcp`, `DELETE /mcp` are available
- Better for long-running integrations

Note: Unlike some server implementations, this server does not currently expose configuration knobs for session TTL or server pooling. In stateful mode, sessions persist until explicitly terminated or the server restarts.

### Security Settings

These settings protect against DNS rebinding by validating the `Host` and `Origin` headers.

| Variable | Description |
|----------|-------------|
| `MCP_ALLOWED_ORIGINS` | Comma-separated allowed `Origin` values. Empty or `*` disables checks. |
| `MCP_ALLOWED_HOSTS` | Comma-separated allowed `Host` values. Empty or `*` disables checks. |

Example:

```bash
MCP_ALLOWED_ORIGINS="https://chatgpt.com,https://platform.openai.com,https://your-subdomain.example.com" \
MCP_ALLOWED_HOSTS="your-subdomain.example.com" \
  uv run amazon-bedrock-knowledge-base-mcp
```

---

## HTTPS for Production

ChatGPT and other external clients require HTTPS. Use nginx as a reverse proxy:

```nginx
server {
    listen 443 ssl;
    server_name your-subdomain.example.com;

    ssl_certificate /etc/letsencrypt/live/your-subdomain.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-subdomain.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

> **Tip:** Use [Certbot](https://certbot.eff.org/) to obtain free Let's Encrypt certificates.
>
> nginx docs: https://nginx.org/en/docs/

### Local Development with ngrok

For local testing with ChatGPT, use [ngrok](https://ngrok.com/) to expose your server:

```bash
ngrok http 8000
```

ngrok provides a public HTTPS URL that tunnels to your local server.

---

## Health Checks

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Basic health check (always returns ok) |
| `GET /health/ready` | Readiness check (verifies AWS credentials via STS) |

Example responses:

```json
// GET /health
{
  "status": "ok",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "service": "amazon-bedrock-knowledge-base-mcp",
  "version": "0.x.x"
}

// GET /health/ready
{
  "status": "ready",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "service": "amazon-bedrock-knowledge-base-mcp",
  "version": "0.x.x"
}
```

---

## Local Development

### Prerequisites

- Python 3.10+
- `uv`

### Clone and Install

```bash
git clone https://github.com/Zlash65/amazon-bedrock-knowledge-base-mcp.git
cd amazon-bedrock-knowledge-base-mcp
uv sync --group dev
```

### Run HTTP Server from Source

```bash
AWS_REGION=us-west-2 \
MCP_TRANSPORT=streamable-http \
MCP_HOST=0.0.0.0 \
PORT=8000 \
MCP_STATELESS=true \
  uv run amazon-bedrock-knowledge-base-mcp
```

### Development Workflow

```bash
# Watch mode for Python (re-run on changes)
AWS_REGION=us-west-2 MCP_TRANSPORT=streamable-http MCP_HOST=0.0.0.0 PORT=8000 MCP_STATELESS=true \
  uv run --with watchfiles watchfiles "uv run amazon-bedrock-knowledge-base-mcp"

# In another terminal, run the HTTP server
AWS_REGION=us-west-2 MCP_TRANSPORT=streamable-http MCP_HOST=0.0.0.0 PORT=8000 MCP_STATELESS=true \
  uv run amazon-bedrock-knowledge-base-mcp

uv run ruff check .
uv run pytest -q
```

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# MCP initialize (stateless mode)
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test", "version": "1.0.0"}
    }
  }'
```

### Docker Development

Build and run the HTTP server container:

```bash
# Build
docker build -t amazon-bedrock-knowledge-base-mcp:local .

# Run
docker run -p 8000:8000 \
  -e AWS_REGION="us-west-2" \
  -e MCP_TRANSPORT="streamable-http" \
  -e MCP_HOST="0.0.0.0" \
  -e PORT="8000" \
  -e MCP_STATELESS="true" \
  amazon-bedrock-knowledge-base-mcp:local
```

---

### Test AWS Credentials with Docker

The easiest way to validate credentials end-to-end is:

```bash
curl http://localhost:8000/health/ready
```

If you want to validate your host AWS credentials independently (outside the MCP server), you can use
the AWS CLI container:

```bash
docker run --rm \
  -v "$HOME/.aws:/root/.aws:ro" \
  -e AWS_PROFILE=your-profile \
  amazon/aws-cli sts get-caller-identity
```

---

## OAuth Authentication

For ChatGPT integration with OAuth, see [ChatGPT Setup Guide](chatgpt-setup.md).

Quick overview:

```bash
MCP_TRANSPORT=streamable-http \
MCP_AUTH_MODE=oauth \
AUTH0_DOMAIN=your-tenant.us.auth0.com \
AUTH0_AUDIENCE=https://your-subdomain.example.com/mcp \
MCP_RESOURCE_URL=https://your-subdomain.example.com/mcp \
  uv run amazon-bedrock-knowledge-base-mcp
```

---

## Docker Compose Example

```yaml
version: '3.8'

services:
  mcp-http:
    build:
      context: .
    ports:
      - "8000:8000"
    environment:
      AWS_REGION: us-west-2
      MCP_TRANSPORT: streamable-http
      MCP_HOST: 0.0.0.0
      PORT: 8000
      MCP_STATELESS: "true"
      # Optional (recommended)
      # MCP_ALLOWED_HOSTS: your-subdomain.example.com
      # MCP_ALLOWED_ORIGINS: https://chatgpt.com,https://chat.openai.com
    volumes:
      # If you use profiles on the host, mount credentials into the container
      - ~/.aws:/app/.aws:ro
    command: ["amazon-bedrock-knowledge-base-mcp"]
```

---

## Troubleshooting

### Connection Refused

- Verify the server is running and listening on the expected port
- If running in Docker, confirm you set `MCP_HOST=0.0.0.0` (binding to `127.0.0.1` inside a container
  makes it unreachable from outside)
- If running behind nginx, check the nginx upstream port and reload nginx

### CORS Errors

- Set `MCP_ALLOWED_ORIGINS` to include the client origin (e.g., `https://chatgpt.com`)
- Ensure the client sends the `Origin` header

### 401 Unauthorized

- Verify Auth0 configuration (`AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, `MCP_RESOURCE_URL`)
- Verify OAuth metadata is exposed:
  ```bash
  curl https://your-subdomain.example.com/.well-known/oauth-protected-resource/mcp
  ```

### Session Not Found (Stateful Mode)

- Sessions are only used when `MCP_STATELESS=false`
- Ensure the client sends the `mcp-session-id` header
