from django.contrib.auth import get_user_model

from app.celery import app

User = get_user_model()


@app.task
def get_schedule_data(user_pk: int) -> dict[int, list[str]] | None:
    user = User.objects.filter(pk=user_pk).first()
    if user:
        return user.get_schedule()

    return None
