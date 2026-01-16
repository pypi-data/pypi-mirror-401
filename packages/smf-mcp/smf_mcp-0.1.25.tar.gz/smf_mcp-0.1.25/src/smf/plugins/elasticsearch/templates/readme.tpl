# {server_name}

SMF server with Elasticsearch integration for the `{default_index}` index.

## Setup

1. **Install dependencies:**
   
   Choose the version matching your Elasticsearch cluster:
   ```bash
   # For Elasticsearch 7.x cluster
   uv add smf-mcp[elasticsearch7]
   # or
   pip install smf-mcp[elasticsearch7]
   
   # For Elasticsearch 8.x cluster
   uv add smf-mcp[elasticsearch8]
   # or
   pip install smf-mcp[elasticsearch8]
   
   # For Elasticsearch 9.x cluster (default)
   uv add smf-mcp[elasticsearch9]
   # or
   pip install smf-mcp[elasticsearch9]
   ```
   
   **Note:** The plugin automatically detects version mismatches and provides clear error messages if your client version doesn't match your cluster version.

2. **Configure Elasticsearch connection:**
   
   Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Elasticsearch settings:
   ```bash
   ELASTICSEARCH_HOSTS=http://localhost:9200
   ELASTICSEARCH_API_KEY=your-api-key  # Optional
   ```

3. **Configure authentication (optional but recommended):**
   
   FastMCP can enable auth without changing any code by setting env vars:
   ```bash
   FASTMCP_SERVER_AUTH=smf.auth.providers.oidc.OIDCProxyProvider

   # OIDC discovery (if available)
   # FASTMCP_SERVER_AUTH_OIDC_CONFIG_URL=https://idp.example.com/.well-known/openid-configuration

   # Or explicit endpoints (works with Elastic/PingFederate)
   FASTMCP_SERVER_AUTH_OIDC_AUTHORIZATION_ENDPOINT=https://idfed.mpsa.com:443/as/authorization.oauth2
   FASTMCP_SERVER_AUTH_OIDC_TOKEN_ENDPOINT=https://idfed.mpsa.com:443/as/token.oauth2
   FASTMCP_SERVER_AUTH_OIDC_JWKS_URI=https://idfed.mpsa.com:443/pf/JWKS
   FASTMCP_SERVER_AUTH_OIDC_ISSUER=https://idfed.mpsa.com:443

   FASTMCP_SERVER_AUTH_OIDC_CLIENT_ID=your-client-id
   FASTMCP_SERVER_AUTH_OIDC_CLIENT_SECRET=your-client-secret
   FASTMCP_SERVER_AUTH_OIDC_BASE_URL=https://your-mcp-server.example.com
   ```

4. **Start Elasticsearch** (if running locally):
   ```bash
   docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.0.0
   ```

## Usage

### Run the server:
```bash
smf run server.py
```

### Run with HTTP transport:
```bash
smf run server.py --transport http --port 8000
```

### Test with inspector:
```bash
smf inspector server.py
```

## Available Tools

The server provides these read-only Elasticsearch tools:

- **search_tool** - Simple search documents in the `{default_index}` index (text query)
- **get_document_tool** - Get a document by ID
- **list_indices_tool** - List all Elasticsearch indices
- **cluster_health_tool** - Get cluster health information
- **query_dsl_search_tool** - Execute complex Elasticsearch Query DSL queries (full JSON query DSL)
- **esql_query_tool** - Execute ES|QL (Elasticsearch Query Language) queries (SQL-like queries)

All tools are read-only and do not modify data in Elasticsearch.

**Advanced Tools:**
- `query_dsl_search_tool`: Accepts a complete Query DSL JSON string, allowing you to write complex queries with aggregations, sorting, filtering, etc.
- `esql_query_tool`: Accepts ES|QL query strings (SQL-like syntax) for powerful data analysis. Requires Elasticsearch 8.11+ or 9.0+.

## Customization

Edit `server.py` to add additional Elasticsearch tools. Note that the default tools are read-only.
If you need write operations (index, update, delete), you can add them as custom tools in `src/tools/elasticsearch.py`.

## Environment Variables

- `ELASTICSEARCH_HOSTS` - Elasticsearch host(s) (default: {es_hosts})
- `ELASTICSEARCH_API_KEY` - API key for authentication (optional)
- `ELASTICSEARCH_USERNAME` - Username for basic auth (optional, used with ELASTICSEARCH_PASSWORD)
- `ELASTICSEARCH_PASSWORD` - Password for basic auth (optional, used with ELASTICSEARCH_USERNAME)
- `ELASTICSEARCH_BASIC_AUTH` - Basic auth as JSON array `["username", "password"]` (alternative to USERNAME/PASSWORD)
- `ELASTICSEARCH_VERIFY_CERTS` - Verify SSL certificates (default: true). Set to `false` to disable SSL verification.
- `ELASTICSEARCH_TIMEOUT` - Request timeout in seconds
- `ELASTICSEARCH_MAX_RETRIES` - Maximum retries (default: 3)
- `ELASTICSEARCH_COMPATIBILITY_VERSION` - Expected major version (7, 8, or 9) for validation (optional)

**Auth (optional):**
- `FASTMCP_SERVER_AUTH` - Set to `smf.auth.providers.oidc.OIDCProxyProvider`
- `FASTMCP_SERVER_AUTH_OIDC_CONFIG_URL` - OIDC discovery URL (optional)
- `FASTMCP_SERVER_AUTH_OIDC_AUTHORIZATION_ENDPOINT` - OAuth authorize endpoint
- `FASTMCP_SERVER_AUTH_OIDC_TOKEN_ENDPOINT` - OAuth token endpoint
- `FASTMCP_SERVER_AUTH_OIDC_JWKS_URI` - JWKS URL for JWT verification
- `FASTMCP_SERVER_AUTH_OIDC_ISSUER` - Token issuer
- `FASTMCP_SERVER_AUTH_OIDC_CLIENT_ID` - OAuth client ID
- `FASTMCP_SERVER_AUTH_OIDC_CLIENT_SECRET` - OAuth client secret
- `FASTMCP_SERVER_AUTH_OIDC_BASE_URL` - Public URL of this MCP server
- `FASTMCP_SERVER_AUTH_OIDC_REQUIRED_SCOPES` - Required scopes (comma or space-separated)

## Documentation

- [SMF Documentation](https://github.com/guinat/smf-mcp)
- [FastMCP Documentation](https://fastmcp.wiki/)
- [Elasticsearch Python Client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
