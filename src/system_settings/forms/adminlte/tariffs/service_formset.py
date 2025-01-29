from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet

from src.system_settings.models import Tariff, TariffService, Service


class ServiceSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-unit"] = value.instance.unit.unit
        return option


class AdminTariffServiceForm(forms.ModelForm):
    price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0.0, 'step': 0.1}),
        label='Ціна'
    )

    def clean(self):
        has_price = bool(self.cleaned_data.get('price'))
        has_service = bool(self.cleaned_data.get('service'))

        if has_price != has_service:
            raise ValidationError('Не вказано ціну або не обрано послугу')

    class Meta:
        model = TariffService

        widgets = {
            'service': ServiceSelect(attrs={'class': 'form-control'}),
        }

        labels = {
            'service': 'Послуга',
        }

        fields = ('service', 'price')

    def __init__(self, *args, **kwargs):
        service_choices = kwargs.pop('service_choices', [])

        super(AdminTariffServiceForm, self).__init__(*args, **kwargs)

        self.fields['service'].choices = service_choices


class BaseAdminTariffServiceFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = Service.objects.select_related('unit').all()

        self.service_choices = [*forms.ModelChoiceField(
            queryset=qs,
            empty_label='Виберіть...',
        ).choices]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['service_choices'] = self.service_choices
        return kwargs


AdminTariffServiceFormSet = inlineformset_factory(
    parent_model=Tariff,
    model=TariffService,
    form=AdminTariffServiceForm,
    formset=BaseAdminTariffServiceFormSet,
    can_delete=True,
    can_delete_extra=True,
    extra=1,
)
