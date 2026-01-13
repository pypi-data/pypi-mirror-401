# Deployment Guide

This guide walks you through deploying the Amazon Bedrock Knowledge Base MCP server on a Linux server with HTTPS.

---

## Prerequisites

- A Linux server (Ubuntu 22.04/24.04 recommended) — AWS EC2, DigitalOcean, Linode, etc.
- A registered domain name
- Firewall allowing ports 22 (SSH), 80 (HTTP), and 443 (HTTPS)
- AWS credentials on the server with access to Amazon Bedrock Knowledge Bases (recommended: IAM role on
  EC2 — see [IAM roles for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html))
- At least one Amazon Bedrock Knowledge Base you can retrieve from (see
  [Knowledge Bases for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
- If you are using OAuth: Auth0 configured (complete [ChatGPT Setup Guide](chatgpt-setup.md) Steps 3.1–3.6 first)

---

## Step 1: Configure DNS

Create an A record pointing your domain to your server:

| Type | Name | Value |
|------|------|-------|
| A | your-subdomain | Server Public IP |

Verify DNS propagation:

```bash
nslookup your-subdomain.example.com
```

---

## Step 2: Connect to Server

```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

---

## Step 3: Install Dependencies

Update system packages:

```bash
sudo apt update && sudo apt upgrade -y
```

Install nginx and Certbot:

```bash
sudo apt install -y nginx
sudo apt install -y certbot python3-certbot-nginx
```

Install Python tooling:

```bash
sudo apt install -y python3-venv python3-pip
```

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

source ~/.bashrc
uv --version
```

See: [uv docs](https://docs.astral.sh/uv/) and
[uv installation](https://docs.astral.sh/uv/getting-started/installation/).

---

## Step 4: Configure nginx

Create nginx configuration:

```bash
sudo vim /etc/nginx/sites-available/mcp
```

Add the following (replace `your-subdomain.example.com` with your domain):

```nginx
server {
    listen 80;
    server_name your-subdomain.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Enable the site and reload nginx:

```bash
sudo ln -s /etc/nginx/sites-available/mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Step 5: Obtain SSL Certificate

Run Certbot to obtain and configure SSL:

```bash
sudo certbot --nginx -d your-subdomain.example.com
```

> **Tip:** See [Certbot](https://certbot.eff.org/) for more installation and nginx configuration
> details.

Verify auto-renewal is configured:

```bash
sudo certbot renew --dry-run
```

Certbot automatically updates your nginx config with SSL settings.

---

## Step 6: Install MCP Server

Create app directory:

```bash
sudo mkdir -p /opt/mcp-server
sudo chown ubuntu:ubuntu /opt/mcp-server
```

Clone and install from source:

```bash
cd /opt/mcp-server
git clone https://github.com/Zlash65/amazon-bedrock-knowledge-base-mcp.git

cd amazon-bedrock-knowledge-base-mcp
uv sync
```

---

## Step 7: Configure Environment

Create environment file:

```bash
vim /opt/mcp-server/amazon-bedrock-knowledge-base-mcp/.env
```

Add your configuration:

```bash
# AWS (recommended: IAM role on EC2, otherwise profile/credentials)
AWS_REGION=us-west-2
# AWS_PROFILE=your-profile-name

# Knowledge base discovery
# KB_INCLUSION_TAG_KEY=mcp-multirag-kb

# Retrieval defaults
# BEDROCK_KB_RERANKING_ENABLED=false
# BEDROCK_KB_SEARCH_TYPE=DEFAULT

# Filtering (optional)
# BEDROCK_KB_FILTER_MODE=explicit_then_implicit
# BEDROCK_KB_ALLOW_RAW_FILTER=false

# Streamable HTTP (required for remote clients)
MCP_TRANSPORT=streamable-http
MCP_HOST=127.0.0.1
PORT=8000
MCP_STATELESS=true

# Transport security (DNS rebinding protection)
MCP_ALLOWED_HOSTS=your-subdomain.example.com
MCP_ALLOWED_ORIGINS=https://your-subdomain.example.com

# Optional filtering schemas (use absolute paths)
# BEDROCK_KB_SCHEMA_DEFAULT_PATH=/etc/amazon-bedrock-knowledge-base-mcp/schemas/default.schema.json
# BEDROCK_KB_SCHEMA_MAP_JSON=/etc/amazon-bedrock-knowledge-base-mcp/schemas/schema-map.json

# Auth0 OAuth
MCP_AUTH_MODE=oauth
AUTH0_DOMAIN=your-tenant.us.auth0.com
AUTH0_AUDIENCE=https://your-subdomain.example.com/mcp
MCP_RESOURCE_URL=https://your-subdomain.example.com/mcp
```

---

## Step 8: Create systemd Service

Create service file:

```bash
sudo vim /etc/systemd/system/amazon-bedrock-knowledge-base-mcp.service
```

Add the following (update paths if different):

```ini
[Unit]
Description=Amazon Bedrock Knowledge Base MCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/mcp-server/amazon-bedrock-knowledge-base-mcp
EnvironmentFile=/opt/mcp-server/amazon-bedrock-knowledge-base-mcp/.env
ExecStart=/opt/mcp-server/amazon-bedrock-knowledge-base-mcp/.venv/bin/amazon-bedrock-knowledge-base-mcp
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable amazon-bedrock-knowledge-base-mcp
sudo systemctl start amazon-bedrock-knowledge-base-mcp
```

---

## Step 9: Verify Deployment

Check service status:

```bash
sudo systemctl status amazon-bedrock-knowledge-base-mcp
```

View logs:

```bash
sudo journalctl -u amazon-bedrock-knowledge-base-mcp -f
```

Test health endpoint:

```bash
curl https://your-subdomain.example.com/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2025-12-27T...",
  "service": "amazon-bedrock-knowledge-base-mcp",
  "version": "0.x.x"
}
```

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `sudo systemctl status amazon-bedrock-knowledge-base-mcp` | Check service status |
| `sudo systemctl restart amazon-bedrock-knowledge-base-mcp` | Restart service |
| `sudo systemctl stop amazon-bedrock-knowledge-base-mcp` | Stop service |
| `sudo journalctl -u amazon-bedrock-knowledge-base-mcp -f` | View live logs |
| `sudo journalctl -u amazon-bedrock-knowledge-base-mcp --since "1 hour ago"` | View recent logs |
| `sudo nginx -t` | Test nginx config |
| `sudo systemctl reload nginx` | Reload nginx |
| `sudo certbot renew` | Renew SSL certificate |

---

## Next Steps

1. **Connect ChatGPT** — Complete Step 4 in the [ChatGPT Setup Guide](chatgpt-setup.md)
2. **Monitor** — Set up monitoring for your server (UptimeRobot, Datadog, etc.)
