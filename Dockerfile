FROM python:3.12-slim-bookworm

RUN useradd -m -u 1000 mcpuser

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

CMD ["uvicorn", "server:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
