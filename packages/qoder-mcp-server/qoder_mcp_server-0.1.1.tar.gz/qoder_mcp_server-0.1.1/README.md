# Qoder MCP Server

A custom MCP (Model Context Protocol) server for Qoder, providing file operations and DashScope integration.

## Features

- **DashScope Integration**: Tools to check API key and call DashScope generation.
- **File System**: Basic file system operations (e.g., `pwd`).

## Installation

You can install this package directly or run it using `uvx`.

### Using uvx

```bash
uvx qoder-mcp-server
```

### Manual Installation

```bash
pip install qoder-mcp-server
```

## Configuration

Ensure you have the following environment variables set:

- `DASHSCOPE_API_KEY`: Your DashScope API key.

## Usage

This server is intended to be used with an MCP client (like Qoder or Claude Desktop).

To run it locally:

```bash
qoder-mcp-server
```
