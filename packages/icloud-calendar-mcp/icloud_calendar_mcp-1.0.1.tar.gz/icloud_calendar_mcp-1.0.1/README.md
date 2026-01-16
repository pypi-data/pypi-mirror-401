# iCloud Calendar MCP Server

A security-first MCP (Model Context Protocol) server for iCloud Calendar access via CalDAV.

## Installation

```bash
# Using uvx (recommended)
uvx icloud-calendar-mcp

# Using pip
pip install icloud-calendar-mcp
icloud-calendar-mcp
```

## Requirements

- **Java 17+** must be installed
- **iCloud credentials** (Apple ID + App-Specific Password)

## Setup

### 1. Get an App-Specific Password

1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign in and go to **Security** → **App-Specific Passwords**
3. Generate a new password for "iCloud Calendar MCP"

### 2. Set Environment Variables

```bash
export ICLOUD_USERNAME="your-apple-id@icloud.com"
export ICLOUD_PASSWORD="your-app-specific-password"
```

### 3. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "icloud-calendar": {
      "command": "uvx",
      "args": ["icloud-calendar-mcp"],
      "env": {
        "ICLOUD_USERNAME": "your-apple-id@icloud.com",
        "ICLOUD_PASSWORD": "your-app-specific-password"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `list_calendars` | List all available calendars |
| `get_events` | Get events from a calendar |
| `create_event` | Create a new calendar event |
| `update_event` | Update an existing event |
| `delete_event` | Delete an event |

## Security

- Uses App-Specific Passwords (never your main Apple ID password)
- Credentials are only used for CalDAV authentication
- No data is stored or transmitted to third parties

## Links

- [GitHub Repository](https://github.com/icloud-calendar-mcp/icloud-calendar-mcp)
- [npm Package](https://www.npmjs.com/package/@icloud-calendar-mcp/server)
- [MCP Documentation](https://modelcontextprotocol.io)

## License

Apache-2.0
