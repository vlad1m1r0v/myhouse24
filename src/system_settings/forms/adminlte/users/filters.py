from django import forms
from django.forms import widgets
from django.contrib.auth.models import Group

from src.authentication.models import STATUS_CHOICES


class AdminUsersFiltersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['role'].choices = [(group.name, group.name) for group in Group.objects.all()] + [('', 'Виберіть...')]

    name = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    role = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
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
