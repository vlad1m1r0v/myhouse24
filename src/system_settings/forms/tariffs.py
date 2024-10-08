from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

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
    price = forms.DecimalField(
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

    def clean(self):
        has_price = bool(self.cleaned_data.get('price'))
        has_service = bool(self.cleaned_data.get('service'))

        if has_price != has_service:
            raise ValidationError('Не вказано ціну або не обрано послугу')


    class Meta:
        model = TariffService
        fields = ('service', 'price')


AdminTariffServiceFormSet = inlineformset_factory(
    parent_model=Tariff,
    model=TariffService,
    form=AdminTariffServiceForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1,
)



