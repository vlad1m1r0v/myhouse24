from django import forms
from django.forms import widgets


class AdminFlatsFiltersForm(forms.Form):
    house = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    section = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    floor = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    flat = forms.CharField(
        widget=widgets.NumberInput(attrs={"class": "form-control", "style": "width: 100%"}),
    )

    flat_owner = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    has_debt = forms.ChoiceField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        choices=[
            ('true', 'Є борг'),
            ('false', 'Немає боргу'),
            ('', 'Виберіть...')
        ]
    )
