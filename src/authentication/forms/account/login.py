from django import forms
from django_recaptcha.fields import ReCaptchaField


class AccountLoginForm(forms.Form):
    login = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Електронна пошта або ID',
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control'
            }
        ))

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control'}
    ))

    captcha = ReCaptchaField(error_messages={
        'required': 'Ви не пройшли перевірку ReCaptcha'
    })
