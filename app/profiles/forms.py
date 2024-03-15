from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import Select, SelectMultiple

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'full_name', 'institute', 'course', 'group'
