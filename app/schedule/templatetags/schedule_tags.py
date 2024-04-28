from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_note(context, table_name, day, lesson_number):
    user = context.get('user')
    day = datetime.strptime(day, '%Y-%m-%d')
    return user.notes.filter(schedule_name=table_name, group=user.group, day=day, lesson_number=lesson_number).first()
