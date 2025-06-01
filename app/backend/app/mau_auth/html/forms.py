from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from schedule.models import MauInstitute

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "full_name", "email", "password", "course", "institute", "group"
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "config-input form-control", "placeholder": "full_name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "config-input form-control", "placeholder": "email"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "config-input form-control", "placeholder": "password"}
            ),
            "course": forms.NumberInput(
                attrs={"class": "config-input form-control", "placeholder": "course"}
            ),
            "group": forms.TextInput(
                attrs={"class": "config-input form-control", "placeholder": "group"}
            ),
        }
        labels = {"password": "Пароль"}

    institute = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={"class": "config-select form-select", "placeholder": "institute"}
        ),
        queryset=MauInstitute.objects.all(),
        empty_label="Открыть меню",
        to_field_name="name",
        label="Институт",
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "config-input form-control",
                "placeholder": "example@example.com",
            }
        ),
        label="Email",
        label_suffix="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "config-input form-control", "placeholder": "password"}
        ),
        label="Пароль",
        label_suffix="",
    )

    error_messages = {
        "invalid_login": "Введите правильный логин и пароль.",
        "inactive": "Этот аккаунт неактивен.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and email:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                for field in self.fields.values():
                    field.widget.attrs["class"] += " error-config-input"

                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "config-input form-control", "placeholder": "Ввод"}
        ),
        label="Email",
        label_suffix="",
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "class": "config-input form-control",
                "placeholder": "password1",
                "autocomplete": "new-password",
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        label_suffix="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "config-input form-control",
                "placeholder": "password2",
                "autocomplete": "new-password",
            }
        ),
    )
