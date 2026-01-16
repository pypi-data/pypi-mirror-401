# {project_name}

SMF MCP server project.

## Setup

1. **Install dependencies:**
   ```bash
   uv add smf-mcp
   # or
   pip install smf-mcp
   ```

2. **Add your tools:**
   
   Edit `src/tools/tools.py` to add your custom tools.

3. **Configure authentication (optional but recommended):**
   
   You can enable auth without code changes by setting env vars:
   ```bash
   FASTMCP_SERVER_AUTH=smf.auth.providers.oidc.OIDCProxyProvider
   FASTMCP_SERVER_AUTH_OIDC_CONFIG_URL=https://idp.example.com/.well-known/openid-configuration
   FASTMCP_SERVER_AUTH_OIDC_CLIENT_ID=your-client-id
   FASTMCP_SERVER_AUTH_OIDC_CLIENT_SECRET=your-client-secret
   FASTMCP_SERVER_AUTH_OIDC_BASE_URL=https://your-mcp-server.example.com
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

## Project Structure

```
{project_name}/
├── src/
│   └── tools/
│       ├── __init__.py
│       └── tools.py          # Your tools
├── server.py                  # Main server file
└── README.md                  # This file
```

## Adding Tools

Add tools to `src/tools/tools.py`:

```python
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"
```

Then register them in `server.py`:

```python
from tools.tools import my_tool

@mcp.tool
def my_tool_wrapper(param: str) -> str:
    """Tool description."""
    return my_tool(param)
```

## Documentation

- [SMF Documentation](https://github.com/guinat/smf-mcp)
- [FastMCP Documentation](https://fastmcp.wiki/)
