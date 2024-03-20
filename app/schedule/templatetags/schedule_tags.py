from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def check_user_note(context, day, lesson_number):
    user = context.get('user')
    day = datetime.strptime(day, '%Y-%m-%d')
    return user.notes.filter(day=day, lesson_number=lesson_number).exists()
