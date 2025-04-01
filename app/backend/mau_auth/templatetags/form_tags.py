from typing import Optional

from django import template
from django.forms import BoundField, ModelChoiceField

register = template.Library()


@register.simple_tag
def clear_label_suffix(field: BoundField) -> BoundField:
    field.field.label_suffix = ""
    return field
