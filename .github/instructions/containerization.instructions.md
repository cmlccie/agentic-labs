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
- Make scripts executable with `RUN chmod +x <script>`
- Use `ENTRYPOINT` for the main command and `CMD` for default arguments

### Security & Operations

- Don't run as root user when possible
- Use `--no-cache-dir` with pip to reduce image size
- Expose only necessary ports
- Include health checks when appropriate
- Use `.dockerignore` to exclude unnecessary files

### Dependencies

- Generate `requirements.txt` using `uv export --only-group <group-name>`
- Include hash verification for security
- Pin all dependency versions for reproducibility

## Example Dockerfile Pattern

```dockerfile
# Use Python 3.13 with Alpine Linux for a lightweight image
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script
COPY <script_name>.py .

# Make the script executable
RUN chmod +x <script_name>.py

# Expose port if needed (e.g., for HTTP services)
EXPOSE 8000

# Set the entry point to run the application
# Default to stdio mode, but can be overridden
ENTRYPOINT ["python", "<script_name>.py"]
CMD ["<default_arg>"]
```
