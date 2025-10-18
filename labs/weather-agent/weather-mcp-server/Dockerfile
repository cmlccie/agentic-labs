# Use Python 3.13 with Alpine Linux for a lightweight image
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MCP server script
COPY weather_mcp_server.py .

# Make the script executable
RUN chmod +x weather_mcp_server.py

# Expose port 8000 for HTTP transport (if using streamable-http mode)
EXPOSE 8000

# Set the entry point to run the MCP server
# Default to stdio mode, but can be overridden
ENTRYPOINT ["python", "weather_mcp_server.py"]
CMD ["stdio"]
