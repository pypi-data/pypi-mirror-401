# Docs

Setup and deployment guides for `amazon-bedrock-knowledge-base-mcp`.

If you’re not sure where to start:

1. Local desktop usage: [stdio-setup.md](stdio-setup.md)
2. Remote server usage: [streamable-http.md](streamable-http.md)
3. Full Linux deployment (systemd + nginx + HTTPS): [server-setup.md](server-setup.md)
4. ChatGPT connector (Auth0 OAuth): [chatgpt-setup.md](chatgpt-setup.md)

## Files

- [stdio-setup.md](stdio-setup.md): STDIO mode (Claude Desktop + local MCP clients)
- [streamable-http.md](streamable-http.md): Streamable HTTP mode (remote MCP server)
- [server-setup.md](server-setup.md): deploy behind nginx + certbot + systemd
- [chatgpt-setup.md](chatgpt-setup.md): Auth0 OAuth setup for ChatGPT

## Useful Links

- `uv` / `uvx`: https://docs.astral.sh/uv/ and https://docs.astral.sh/uv/getting-started/installation/
- Amazon Bedrock Knowledge Bases: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- AWS CLI config files (profiles): https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
- Auth0: https://auth0.com
- ChatGPT: https://chatgpt.com/
- Certbot: https://certbot.eff.org/
- ngrok: https://ngrok.com/
- Claude Desktop: https://claude.com/download

## Assets

This repo includes `assets/` (screenshots/diagrams) used by the guides.
