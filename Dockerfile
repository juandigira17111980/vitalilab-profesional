FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system --gid 10001 vitalilab && \
    adduser --system --uid 10001 --ingroup vitalilab --no-create-home vitalilab

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R vitalilab:vitalilab /app

USER vitalilab
EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:10000/ready', timeout=3)"]

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:10000", "--workers", "1", "--threads", "4", "--timeout", "60", "--access-logfile", "-", "--access-logformat", "method=%(m)s status=%(s)s duration=%(L)s", "--error-logfile", "-"]
