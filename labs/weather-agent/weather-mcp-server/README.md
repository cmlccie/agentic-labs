# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information capabilities.

## Docker Image

This project is automatically built and published as a multi-architecture Docker image supporting both `amd64` and `arm64` platforms.

### Available Images

- `ghcr.io/cmlccie/agentic-labs/weather-mcp-server:latest` - Latest version from main branch
- `ghcr.io/cmlccie/agentic-labs/weather-mcp-server:main` - Main branch builds
- `ghcr.io/cmlccie/agentic-labs/weather-mcp-server:v*` - Tagged releases

### Usage

#### Running with Docker

```bash
# Run in stdio mode (default)
docker run --rm ghcr.io/cmlccie/agentic-labs/weather-mcp-server:latest

# Run in HTTP mode on port 8000
docker run --rm -p 8000:8000 ghcr.io/cmlccie/agentic-labs/weather-mcp-server:latest http
```

#### Running with Docker Compose

```yaml
version: "3.8"
services:
  weather-mcp-server:
    image: ghcr.io/cmlccie/agentic-labs/weather-mcp-server:latest
    ports:
      - "8000:8000"
    command: ["http"]
```

## Building Locally

```bash
# Build for your current platform
docker build -t weather-mcp-server .

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t weather-mcp-server .
```

## Development

This MCP server is built with:

- Python 3.13
- Alpine Linux base image
- Multi-architecture support (amd64, arm64)

See `requirements.txt` for Python dependencies and `weather_mcp_server.py` for the server implementation.
