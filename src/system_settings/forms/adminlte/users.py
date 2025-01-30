from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import transaction

from src.authentication.models import CustomUser, STATUS_CHOICES
from src.system_settings.tasks import send_password_update_notification


class AdminUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ім\'я')

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Прізвище')

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефону')

    role = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Роль",
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус')

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Електронна пошта'
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Новий пароль', 'class': 'form-control'}),
        required=False,
        label="Новий пароль"
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль', 'class': 'form-control'}),
        required=False,
        label="Повторіть пароль"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'status', 'new_password', 'repeat_password']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')

        super().__init__(*args, **kwargs)

        self.fields['role'].choices = [(role.id, role.name) for role in Group.objects.all()]

        if not user:
            self.fields['new_password'].required = True
            self.fields['repeat_password'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (CustomUser.objects.filter(email=email)
                .exclude(pk=self.instance.pk if self.instance else None).exists()):
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

        user.is_staff = True

        selected_group = self.cleaned_data.get('role')

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

        if self.instance.pk:
            user.groups.clear()

        if commit:
            user.save()

        if selected_group:
            user.groups.add(selected_group)

        return user
