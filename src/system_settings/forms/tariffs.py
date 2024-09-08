from django import forms
from django.forms import modelformset_factory

from src.system_settings.models import Tariff, TariffService, Service


class AdminTariffForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Назва тарифу')
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 5,
                   'style': 'resize: none;'
                   }),
        label='Опис тарифу')

    class Meta:
        model = Tariff
        fields = ('name', 'description')


class AdminTariffServiceForm(forms.ModelForm):
    price = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ціна'
    )

    service = forms.ModelChoiceField(
        required=False,
        queryset=Service.objects.all(),
        label='Послуга',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Виберіть...'
    )

    class Meta:
        model = TariffService
        fields = ('service', 'price')


AdminTariffServiceFormSet = modelformset_factory(
    model=TariffService,
    form=AdminTariffServiceForm,
    can_delete=True,
    extra=1,
)



