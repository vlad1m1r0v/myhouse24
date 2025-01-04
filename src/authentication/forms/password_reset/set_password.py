from django import forms
from django.contrib.auth.forms import SetPasswordForm


class AuthenticationSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введіть новий пароль', 'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Повторіть пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль', 'class': 'form-control'}),
        strip=False,
    )