from django import forms
from django.forms import widgets

from src.meter_indicators.models import StatusChoices


class AdminMeterIndicatorsForFlatFiltersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial = kwargs.get('initial', {})

        service = initial.get('service')

        if service:
            self.fields['service'].widget.choices = [(service.id, service.name)]


    no = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    date = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    status = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
        choices=StatusChoices.choices + [('', 'Виберіть...')],
    )

    service = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
