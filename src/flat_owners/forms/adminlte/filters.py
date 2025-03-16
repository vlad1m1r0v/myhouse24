from django import forms
from django.forms import widgets

from src.authentication.models import STATUS_CHOICES


class AdminFlatOwnersFiltersForm(forms.Form):
    ID = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    full_name = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    email = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    house = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    flat = forms.CharField(
        widget=widgets.NumberInput(attrs={"class": "form-control"})
    )

    date_joined = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    status = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
        choices=STATUS_CHOICES + [('', 'Виберіть...')],
    )

    has_debt = forms.ChoiceField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        choices=[
            ('true', 'так'),
            ('false', 'ні'),
            ('', 'Виберіть...')
        ]
    )
