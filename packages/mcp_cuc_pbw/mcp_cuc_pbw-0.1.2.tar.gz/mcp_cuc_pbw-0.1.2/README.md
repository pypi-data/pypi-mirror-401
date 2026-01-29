# mcp_cuc_pbw

A simple MCP (Model Context Protocol) Server implementation in Python that provides a tool to get the current time with optional timezone support.

## Version Compatibility

Requires Python 3.10 or higher.

## Features

- Provides a `get_current_time` tool to retrieve the current time
- Supports optional timezone parameter
- Simple and lightweight implementation
- Clear documentation and examples

## Requirements

- Python 3.10 or higher
- pytz (automatically installed)

## Installation

### From PyPI

```bash
pip install mcp_cuc_pbw
```

### From Source

```bash
pip install -e .
```

## Usage

### Start the Server

```bash
mcp-server
```

By default, the server runs on `http://localhost:8000`.

You can specify a different host and port:

```bash
mcp-server --host 0.0.0.0 --port 8080
```

### Using as a Module

```python
from mcp_cuc_pbw import run_server

# Run the server on default host and port
run_server()

# Or specify host and port
run_server(host='0.0.0.0', port=8080)
```

### Available Tools

#### `get_current_time`

Gets the current time with optional timezone support.

**Parameters:**
- `timezone` (optional): Timezone string (e.g., `Asia/Shanghai`, `UTC`, `America/New_York`)

**Example Request:**

```json
{
  "tool": "get_current_time",
  "params": {
    "timezone": "Asia/Shanghai"
  }
}
```

**Example Response:**

```json
{
  "tool": "get_current_time",
  "result": {
    "current_time": "2024-01-16 14:30:45",
    "timezone": "Asia/Shanghai"
  }
}
```

**Without Timezone:**

```json
{
  "tool": "get_current_time"
}
```

**Response:**

```json
{
  "tool": "get_current_time",
  "result": {
    "current_time": "2024-01-16 14:30:45",
    "timezone": "local"
  }
}
```

## MCP Protocol Reference

For more information about the Model Context Protocol:

- [Introduction](https://modelcontextprotocol.io/introduction)
- [Architecture](https://modelcontextprotocol.io/docs/concepts/architecture)
- [Server Development Guide](https://modelcontextprotocol.io/quickstart/server)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md)
