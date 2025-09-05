# Use Python 3.12 slim bookworm as base
FROM python:3.12-slim-bookworm

# Create non-root user
RUN useradd -m -u 1000 mcpuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server/ /app/

# Create data directory and set permissions
ENV DATA_DIR=/data/uploads
RUN mkdir -p /data/uploads && \
    chown -R mcpuser:mcpuser /app /data/uploads

# Switch to non-root user
USER mcpuser

# Create volume for data persistence
VOLUME ["/data/uploads"]

# Expose port
EXPOSE 8080

# Use a more robust startup command
CMD ["uvicorn", "server:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
