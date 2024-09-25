from django.conf import settings


def schedule_data(request):
    return {
        "GROUP_SCHEDULE_NAME": settings.GROUP_SCHEDULE_NAME,
        "TEACHER_SCHEDULE_NAME": settings.TEACHER_SCHEDULE_NAME,
        "SCHEDULE_URL": settings.SCHEDULE_URL,
        "DEVELOPER_URL": settings.DEVELOPER_URL,
    }
