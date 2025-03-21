from datetime import datetime

from django import forms
from django.forms import (
    BaseInlineFormSet,
    inlineformset_factory
)

from src.meter_indicators.models import MeterIndicator, StatusChoices
from src.payment_receipts.models import (
    Receipt,
    ReceiptService
)
from src.system_settings.models import (
    Service,
    MeasurementUnit
)


class ServiceSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option["attrs"]["data-unit-id"] = value.instance.unit.id
        return option


class AdminReceiptServiceForm(forms.ModelForm):
    class Meta:
        model = ReceiptService
        fields = ['meter_indicator', 'service', 'unit', 'price', 'value']

        widgets = {
            'meter_indicator': forms.Select(),
            'service': ServiceSelect(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        service_choices = kwargs.pop('service_choices', [])
        unit_choices = kwargs.pop('unit_choices', [])
        indicator_choices = kwargs.pop('indicator_choices', [])

        super(AdminReceiptServiceForm, self).__init__(*args, **kwargs)

        self.fields['service'].choices = service_choices
        self.fields['unit'].choices = unit_choices
        self.fields['meter_indicator'].choices = indicator_choices


class BaseAdminReceiptServiceFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        service_qs = Service.objects.select_related('unit').all()
        self.service_choices = [*forms.ModelChoiceField(
            queryset=service_qs,
            empty_label='Виберіть...',
        ).choices]

        unit_qs = MeasurementUnit.objects.all()
        self.unit_choices = [*forms.ModelChoiceField(
            queryset=unit_qs,
            empty_label='Виберіть...',
        ).choices]

        indicator_qs = MeterIndicator.objects.all()
        self.indicator_choices = [*forms.ModelChoiceField(
            queryset=indicator_qs,
            empty_label='Виберіть...',
        ).choices]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['service_choices'] = self.service_choices
        kwargs['unit_choices'] = self.unit_choices
        kwargs['indicator_choices'] = self.indicator_choices
        return kwargs


AdminReceiptServiceFormSet = inlineformset_factory(
    parent_model=Receipt,
    model=ReceiptService,
    form=AdminReceiptServiceForm,
    formset=BaseAdminReceiptServiceFormset,
    can_delete=True,
    can_delete_extra=True,
    extra=1
)
