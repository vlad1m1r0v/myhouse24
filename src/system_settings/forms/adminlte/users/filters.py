from django import forms
from django.forms import widgets
from django.contrib.auth.models import Group

from src.authentication.models import STATUS_CHOICES


class AdminUsersFiltersForm(forms.Form):
    name = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    role = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
        choices=[(group.name, group.name) for group in Group.objects.all()] + [('', 'Виберіть...')],
    )

    phone = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    email = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES + [('', 'Виберіть...')],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
