---
applyTo: "**/Dockerfile"
---

# Container Image Instructions

## Docker Best Practices

### Base Images

- Use official Python images with Alpine Linux variants for smaller size: `python:3.13-alpine`
- Pin specific versions for reproducibility
- Use multi-stage builds when creating production images to minimize final image size

### Container Structure

- Set working directory to `/app`
- Copy `requirements.txt` first to leverage Docker layer caching
- Install dependencies before copying application code
- Create non-root user and set ownership before copying application files
- Make scripts executable with `RUN chmod +x <script>`
- Use `ENTRYPOINT` for the main command and `CMD` for default arguments
- When using executable Python scripts with shebang, ENTRYPOINT can reference the script directly

### Security & Operations

- Don't run as root user when possible - create a non-root user and switch to it
- Create user and set ownership before copying application files for better security
- Use `--no-cache-dir` with pip to reduce image size
- Expose only necessary ports
- Include health checks when appropriate
- Use `.dockerignore` with allowlist approach (ignore all `*`, then explicitly include needed files)

### Dependencies

- Generate `requirements.txt` using `uv export --only-group <group-name>`
- Include hash verification for security
- Pin all dependency versions for reproducibility

## Example Dockerfile Pattern

```dockerfile
FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser -D -s /bin/sh appuser
RUN chown -R appuser:appuser /app
USER appuser

COPY <script_name>.py .

RUN chmod +x <script_name>.py

# Expose port if needed (e.g., for HTTP services)
EXPOSE 8000

ENTRYPOINT ["<script_name>.py"]
CMD ["<default_arg>"]
```

## Example .dockerignore Pattern

Use an allowlist approach for maximum security and minimal image size:

```ignore
# Ignore all files
*
# Explicitly include only what's needed
!Dockerfile
!requirements.txt
!<script_name>.py
```
