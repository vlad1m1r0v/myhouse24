from django import forms
from django.contrib.auth.hashers import make_password

from src.authentication.models import CustomUser


class AccountProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення')

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ім\'я')

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Прізвище')

    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='По батькові',
        required=False,
    )

    birth_date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата народження',
        required=False,
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефону',
        required=False
    )

    telegram = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Telegram',
        required=False
    )

    viber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Viber',
        required=False
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Електронна пошта'
    )

    ID = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
        label='ID',
        required=False
    )

    about_me = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Про власника (замітки)',
        required=False
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Новий пароль', 'class': 'form-control'}),
        label="Новий пароль",
        required=False
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль', 'class': 'form-control'}),
        label="Повторіть пароль",
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Користувач з такою електронною поштою вже існує")
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        repeat_password = cleaned_data.get('repeat_password')

        if new_password or repeat_password:
            if new_password != repeat_password:
                raise forms.ValidationError("Паролі не співпадають")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('new_password')

        if password:
            user.password = make_password(password)

        if commit:
            user.save()

        return user

    class Meta:
        model = CustomUser
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'middle_name',
            'birth_date',
            'phone_number',
            'viber',
            'telegram',
            'email',
            'ID',
            'about_me',
            'new_password',
            'repeat_password'
        ]
