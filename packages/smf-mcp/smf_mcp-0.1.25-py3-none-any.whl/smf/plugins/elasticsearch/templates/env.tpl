# Elasticsearch Configuration
# ELASTICSEARCH_HOSTS={es_hosts}
# ELASTICSEARCH_API_KEY=your-api-key-here
# Basic auth options (use one of the following):
# ELASTICSEARCH_USERNAME=your-username
# ELASTICSEARCH_PASSWORD=your-password
# OR
# ELASTICSEARCH_BASIC_AUTH=["username", "password"]
# ELASTICSEARCH_VERIFY_CERTS=true
# ELASTICSEARCH_TIMEOUT=30
# ELASTICSEARCH_MAX_RETRIES=3
# ELASTICSEARCH_COMPATIBILITY_VERSION=9  # Optional: Expected major version (7, 8, or 9) for validation

# FastMCP Auth (generic OIDC/OAuth proxy)
# Set this to enable auth without code changes:
# FASTMCP_SERVER_AUTH=smf.auth.providers.oidc.OIDCProxyProvider
#
# Option A: use OIDC discovery (if your IdP supports it)
# FASTMCP_SERVER_AUTH_OIDC_CONFIG_URL=https://idp.example.com/.well-known/openid-configuration
#
# Option B: explicit endpoints (works with Elastic/PingFederate)
# FASTMCP_SERVER_AUTH_OIDC_AUTHORIZATION_ENDPOINT=
# FASTMCP_SERVER_AUTH_OIDC_TOKEN_ENDPOINT=
# FASTMCP_SERVER_AUTH_OIDC_JWKS_URI=
# FASTMCP_SERVER_AUTH_OIDC_ISSUER=
#
# Client credentials (register a dedicated OAuth app for your MCP server)
# FASTMCP_SERVER_AUTH_OIDC_CLIENT_ID=your-client-id
# FASTMCP_SERVER_AUTH_OIDC_CLIENT_SECRET=your-client-secret
#
# Public URL of this MCP server (used for /auth/* callbacks)
# FASTMCP_SERVER_AUTH_OIDC_BASE_URL=https://your-mcp-server.example.com
#
# Optional
# FASTMCP_SERVER_AUTH_OIDC_AUDIENCE=your-audience
# FASTMCP_SERVER_AUTH_OIDC_REQUIRED_SCOPES=openid
# FASTMCP_SERVER_AUTH_OIDC_REDIRECT_PATH=/auth/callback
# FASTMCP_SERVER_AUTH_OIDC_ALLOWED_CLIENT_REDIRECT_URIS=http://localhost:*,http://127.0.0.1:*
# FASTMCP_SERVER_AUTH_OIDC_JWT_SIGNING_KEY=change-me-in-prod
