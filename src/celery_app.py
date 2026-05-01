"""
Main Celery application configuration.
This module sets up the Celery instance with proper configuration.
"""
from celery import Celery
import os

# Get Redis connection from environment or use default
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6379')
redis_db = os.getenv('REDIS_DB', '0')

broker_url = f'redis://{redis_host}:{redis_port}/{redis_db}'
result_backend = f'redis://{redis_host}:{redis_port}/{redis_db}'

# Create Celery application
app = Celery(
    'celery_demo',
    broker=broker_url,
    backend=result_backend,
    include=[
        'demos.basic_demo',
        'demos.workflows',
        'demos.periodic',
    ]
)

# Configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Retry settings
    broker_connection_retry_on_startup=True,
    # Task settings
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    task_soft_time_limit=240,  # 4 minutes soft limit
)

if __name__ == '__main__':
    app.start()
