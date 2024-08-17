from django.conf import settings


def group_schedule_name(request):
    return {'GROUP_SCHEDULE_NAME': settings.GROUP_SCHEDULE_NAME}


def teacher_schedule_name(request):
    return {'TEACHER_SCHEDULE_NAME': settings.TEACHER_SCHEDULE_NAME}
