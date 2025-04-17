from django import forms
from django.forms import widgets
from django.contrib.auth.models import Group

from src.master_call_requests.models import StatusChoices


class AdminMasterCallRequestFiltersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['master_type'].choices = [(group.id, group.name) for group in Group.objects.filter(name__in=['Сантехнік', 'Електрик'])]

    no = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    date = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    master_type = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
    )

    description = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    flat = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control", "type": "number"}),
    )

    owner = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    master = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    status = forms.ChoiceField(
        choices=StatusChoices.choices + [('', 'Виберіть...')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )
