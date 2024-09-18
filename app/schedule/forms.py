from typing import Iterable

from django import forms


class WeeksForm(forms.Form):
    periods = forms.ChoiceField(label='Период')

    def set_choices(self, field_name: str, value: Iterable) -> None:
        self.fields[field_name].choices = value
