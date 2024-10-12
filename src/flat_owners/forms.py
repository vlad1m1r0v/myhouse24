from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction

from src.authentication.models import CustomUser, STATUS_CHOICES
from src.system_settings.tasks import send_password_update_notification


class AdminFlatOwnerForm(forms.ModelForm):
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
        label='По батькові')

    birth_date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата народження'
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефону')

    telegram = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Telegram'
    )

    viber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Viber'
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Електронна пошта'
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус')

    ID = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='ID'
    )

    about_me = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Про власника (замітки)'
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Новий пароль',
                'class': 'form-control'}),
        required=False,
        label="Новий пароль"
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторіть пароль',
                'class': 'form-control'
            }),
        required=False,
        label="Повторіть пароль"
    )

    class Meta:
        model = CustomUser
        fields = ['avatar',
                  'first_name',
                  'last_name',
                  'middle_name',
                  'birth_date',
                  'phone_number',
                  'viber',
                  'telegram',
                  'email',
                  'status',
                  'ID',
                  'about_me',
                  'new_password',
                  'repeat_password']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if not user:
            self.fields['new_password'].required = True
            self.fields['repeat_password'].required = True

        if user and user.groups.exists():
            self.fields['role'].initial = user.groups.first()

    def clean_ID(self):
        ID = self.cleaned_data.get('ID')
        if CustomUser.objects.filter(ID=ID).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("Користувач з таким ідентифікатором вже існує")
        return ID

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
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

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('new_password')
        if password:
            user.password = make_password(password)

            send_password_update_notification.delay(
                subject_template_name='system_settings/users/password_change_subject.txt',
                email_template_name='system_settings/users/password_change_notification.html',
                context={
                    'email': user.email,
                    'password': password,
                },
                from_email=settings.EMAIL_HOST_USER,
                to_email=user.email
            )

        if commit:
            user.save()

        return user
