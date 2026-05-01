FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set Python path to include src and demos directories
ENV PYTHONPATH=/app

CMD ["celery", "-A", "src.celery_app", "worker", "--loglevel=info"]
