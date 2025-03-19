from django import forms
from django.forms import widgets

from src.personal_accounts.models import STATUS_CHOICES


class AdminPersonalAccountsFiltersForm(forms.Form):
    no = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
    )

    status=forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
        choices= STATUS_CHOICES + [('', 'Виберіть...')],
    )

    flat = forms.CharField(
        widget=widgets.NumberInput(attrs={"class": "form-control", 'style': 'width: 100%'}),
    )

    house = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
    )

    section = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
    )

    owner = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
    )

    has_debt = forms.ChoiceField(
        widget=widgets.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
        choices=[
            ('true', 'Є борг'),
            ('false', 'Немає боргу'),
            ('', 'Виберіть...')
        ]
    )