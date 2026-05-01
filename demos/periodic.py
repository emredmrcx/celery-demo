"""
Periodic tasks demo using Celery Beat.
Showcases scheduled/periodic task execution.
"""

from src.celery_app import app
from celery.schedules import crontab, timedelta
import time
import random
import socket

@app.task(bind=True)
def hourly_health_check(self):
    """Simulate a periodic health check task - runs every hour"""
    start_time = time.strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[periodic] Running health check... | Worker: {worker} | Time: {start_time}")
    time.sleep(2)
    result = {
        'check_time': time.time(),
        'status': 'healthy',
        'services_checked': ['redis', 'worker', 'database'],
        'worker': worker
    }
    print(f"[periodic] Health check completed | Worker: {worker}")
    return result


@app.task(bind=True)
def daily_report_generation(self):
    """Simulate a daily report generation task"""
    start_time = time.strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[periodic] Starting daily report generation... | Worker: {worker} | Time: {start_time}")
    time.sleep(8)
    report_id = f"DAILY-{random.randint(1000, 9999)}"
    result = {
        'report_id': report_id,
        'generated_at': time.time(),
        'type': 'daily_summary',
        'status': 'completed',
        'worker': worker
    }
    print(f"[periodic] Daily report {report_id} generated | Worker: {worker}")
    return result


@app.task(bind=True)
def cleanup_old_data(self):
    """Simulate periodic cleanup task"""
    start_time = time.strftime('%H:%M:%S')
    worker = socket.gethostname()
    print(f"[periodic] Starting cleanup of old data... | Worker: {worker} | Time: {start_time}")
    time.sleep(3)
    result = {
        'cleaned_records': random.randint(50, 500),
        'cleanup_time': time.time(),
        'status': 'completed',
        'worker': worker
    }
    print(f"[periodic] Cleanup completed. Removed {result['cleaned_records']} records | Worker: {worker}")
    return result


# Celery Beat schedule configuration
app.conf.beat_schedule = {
    'hourly-health-check': {
        'task': 'demos.periodic.hourly_health_check',
        'schedule': timedelta(hours=1),  # Run every hour
    },
    'daily-report': {
        'task': 'demos.periodic.daily_report_generation',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
    'weekly-cleanup': {
        'task': 'demos.periodic.cleanup_old_data',
        'schedule': crontab(day_of_week='sunday', hour=2, minute=0),  # Run weekly on Sunday at 2AM
    },
}

app.conf.timezone = 'UTC'
