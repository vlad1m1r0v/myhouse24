from django import forms
from django.contrib.auth.hashers import make_password

from src.authentication.models import CustomUser


class AccountRegisterForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ПІБ'
        }),
    )

    email = forms.EmailField(
        required=True,

        widget=forms.EmailInput(attrs={
            'placeholder': 'Електронна пошта',
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

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторіть пароль',
                'class': 'form-control'
            }
        ))

    privacy_policy_consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control'
        }),
        label='Я погоджуюсь з політикою конфіденційності',
        error_messages={'required': 'Ви повинні погодитися з політикою конфіденційності'}
    )

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name", "").strip()
        words = full_name.split()

        if len(words) not in (2, 3) or any(len(word) < 2 for word in words):
            raise forms.ValidationError(
                "Введіть ім'я та прізвище (або ім'я, прізвище та по батькові), кожне слово повинно містити не менше 2 символів"
            )

        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з такою електронною поштою вже зареєстрований')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password or repeat_password:
            if password != repeat_password:
                raise forms.ValidationError("Паролі не співпадають")

        return cleaned_data

    def save(self, commit=True):
        words = self.cleaned_data["full_name"].split()

        if len(words) == 2:
            last_name, first_name = words
            middle_name = None
        else:
            last_name, first_name, middle_name = words

        email = self.cleaned_data['email']

        password = self.cleaned_data['password']

        user = CustomUser.objects.create(
            # should verify be email
            is_active=False,
            is_staff=False,
            # can be changed by admin
            status='new',
            is_superuser=False,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password=make_password(password)
        )

        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
