from django import forms
from django_recaptcha.fields import ReCaptchaField
from src.authentication.models import CustomUser


class AdminLoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Електронна пошта',
               'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль',
               'class': 'form-control'}
    ))

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control'}
    ))

    captcha = ReCaptchaField(error_messages={
        'required': 'Ви не пройшли перевірку ReCaptcha'
    })

    def clean(self):
        email = self.cleaned_data.get('email')

        try:
            candidate = CustomUser.objects.get(email=email)

            if not candidate.groups.exists():
                raise forms.ValidationError(
                    'Ви не належите до жодної адміністративної групи'
                )

        except CustomUser.DoesNotExist:
            raise forms.ValidationError(
                'Неправильно вказана електронна пошта або пароль'
            )

        return self.cleaned_data