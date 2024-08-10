from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_note(context, table_name, day, lesson_number):
    user = context.get('user')
    return user.notes.filter(schedule_name=table_name, group=user.group, day=day, lesson_number=lesson_number).first()


@register.simple_tag(takes_context=True)
def has_bookmark(context):
    user = context.get('user')
    teacher_name = context.get('teacher_name')
    teacher_key = context.get('teacher_key')
    return user.bookmarks.filter(teacher_name=teacher_name, teacher_key=teacher_key).exists()
