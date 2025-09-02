# will use bookworm until I learn trixie 
FROM python:3.12-slim-bookworm 

RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ /app/

ENV DATA_DIR=/data/uploads
RUN mkdir -p /data/uploads && \
    chown -R mcpuser:mcpuser /app /data/uploads

USER mcpuser

VOLUME ["/data/uploads"]
EXPOSE 8080
# for building purposes only
CMD ["python", "server.py"]
