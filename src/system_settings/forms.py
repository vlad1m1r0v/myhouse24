from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.forms import formset_factory

from src.authentication.models import CustomUser, STATUS_CHOICES
from src.system_settings.models import PaymentItem, TYPE_CHOICES, PaymentCredential
from src.system_settings.tasks import send_password_update_notification


class AdminPaymentItemForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип платежу')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Назва')

    class Meta:
        model = PaymentItem
        fields = ('name', 'type')


class AdminPaymentCredentialForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Назва компанії')
    information = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 4,
                   'style': 'resize: none;'
                   }),
        label='Інформація')

    class Meta:
        model = PaymentCredential
        fields = ('name', 'information')


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

    role = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Group.objects.all(),
        label="Роль",
        empty_label=None
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
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'role', 'status', 'new_password',
                  'repeat_password']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user and user.groups.exists():
            self.fields['role'].initial = user.groups.first()

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


class AdminGroupPermissionForm(forms.Form):
    checkbox = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    permission_id = forms.IntegerField(widget=forms.HiddenInput())
    group_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['checkbox'].initial = self.initial.get('id') is not None

    def save(self):
        group_id = self.cleaned_data['group_id']
        permission_id = self.cleaned_data['permission_id']
        checked = self.cleaned_data['checkbox']

        group = Group.objects.get(id=group_id)
        permission = Permission.objects.get(id=permission_id)

        if checked:
            group.permissions.add(permission)
        else:
            group.permissions.remove(permission)


AdminGroupPermissionFormSet = formset_factory(form=AdminGroupPermissionForm, extra=0)
