FROM python:3.11-slim
WORKDIR /app

COPY pyproject.toml ./
COPY musepicker_ingest ./musepicker_ingest
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "musepicker_ingest.pipeline.run_ingest", "--dry-run"]
