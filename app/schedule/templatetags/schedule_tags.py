from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag()
def prepare_location(table_name, group, day, lesson_number):
    return f"{table_name}:{group}:{day}:{lesson_number}"


@register.simple_tag(takes_context=True)
def get_user_note(context, note_location):
    user = context.get("user")
    return user.notes.filter(location=note_location).first()


@register.simple_tag(takes_context=True)
def has_bookmark(context):
    user = context.get("user")
    teacher_name = context.get("teacher_name")
    teacher_key = context.get("teacher_key")
    return user.bookmarks.filter(
        teacher_name=teacher_name, teacher_key=teacher_key
    ).exists()
