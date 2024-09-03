from cProfile import label

from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from src.authentication.models import CustomUser, STATUS_CHOICES
from src.system_settings.models import PaymentItem, TYPE_CHOICES, PaymentCredential


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


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ім\'я')

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Прізвище')

    role = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Group.objects.all(),
        required=False,
        label="Роль"
    )

    type = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус')

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Електронна пошта'
    )

    password = forms.CharField(
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
        fields = ['first_name', 'last_name', 'email', 'role', 'password', 'repeat_password']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user and user.groups.exists():
            self.fields['role'].initial = user.groups.first()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password or repeat_password:
            if password != repeat_password:
                raise forms.ValidationError("Паролі не співпадають.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        selected_group = self.cleaned_data.get('role')

        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password)

        user.groups.clear()
        if selected_group:
            user.groups.add(selected_group)

        if commit:
            user.save()

        return user
