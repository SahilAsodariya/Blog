
from celery import Celery
from celery.schedules import schedule

celery = Celery("app")
celery.conf.broker_url = "redis://localhost:6379/0"
celery.conf.result_backend = "redis://localhost:6379/0"

# Ensure tasks are loaded
import app.utils.celery_task

# Beat schedule
celery.conf.beat_schedule = {
    "check-subscriptions-every-day": {
        "task": "app.utils.celery_task.check_subscriptions",
        "schedule": schedule(24*60*60),  # run every 1 day
    },
}

celery.conf.timezone = "Asia/Kolkata"




