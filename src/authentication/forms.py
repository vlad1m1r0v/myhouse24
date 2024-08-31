from django import forms
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from src.authentication.models import CustomUser
from src.authentication.tasks import send_reset_password_email


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


class AuthenticationPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Електронна пошта'
        }
    ))

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        send_reset_password_email.delay(subject_template_name=subject_template_name,
                                        email_template_name=email_template_name,
                                        context=context, from_email=from_email, to_email=to_email,
                                        html_email_template_name=html_email_template_name)


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
