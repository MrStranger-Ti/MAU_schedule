import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check_and_delete_note": {
        "task": "notes.tasks.delete_expired_notes",
        "schedule": crontab(minute="0", hour="0"),
    },
}
