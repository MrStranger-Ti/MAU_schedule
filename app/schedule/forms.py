from django import forms


class WeeksForm(forms.Form):
    weeks_periods = forms.ChoiceField()
