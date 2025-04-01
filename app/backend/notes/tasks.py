from datetime import date

from app.celery import app
from notes.models import Note


@app.task
def delete_expired_notes():
    curr_date = date.today()
    expired_notes = Note.objects.filter(expired_date__lte=curr_date)
    expired_notes.delete()
