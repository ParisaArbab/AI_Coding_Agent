FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY app ./app
COPY mcp_server ./mcp_server
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .
RUN useradd --create-home agent && mkdir -p /app/workspace && chown -R agent:agent /app
USER agent
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
