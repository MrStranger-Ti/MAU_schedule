from django import forms
from django.contrib.auth import get_user_model

from mau_auth.models import MauInstitute

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'full_name', 'institute', 'course', 'group'
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'full_name',
            }),
            'course': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'course',
            }),
            'group': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'group',
            }),
        }

    institute = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'institute',
        }),
        queryset=MauInstitute.objects.all(),
        empty_label='Открыть меню',
        to_field_name='name',
        label='Институт',
    )
