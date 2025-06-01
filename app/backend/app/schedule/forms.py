from typing import Iterable

from django import forms


class WeeksForm(forms.Form):
    EMPTY_CHOICE = [("", "Выберите период")]

    periods = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "config-select"}),
    )

    def set_period_choices(self, choices: Iterable) -> None:
        self._get_empty_choice()
        self.fields["periods"].choices += choices

    def _get_empty_choice(self):
        self.fields["periods"].choices = self.EMPTY_CHOICE
