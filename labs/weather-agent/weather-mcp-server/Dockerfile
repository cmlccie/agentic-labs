FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY weather_mcp_server.py .
RUN chmod +x weather_mcp_server.py

RUN adduser -D -s /bin/sh appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port 8000 for HTTP transport (when using streamable-http mode)
EXPOSE 8000

ENTRYPOINT ["weather_mcp_server.py"]
CMD ["stdio"]
