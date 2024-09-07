from django import forms

from src.system_settings.models import MeasurementUnit, Service


class AdminMeasurementUnitForm(forms.ModelForm):
    unit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Одиниця вимірювання'
    )

    class Meta:
        model = MeasurementUnit
        fields = ['unit']


AdminMeasurementUnitFormSet = forms.modelformset_factory(
    model=MeasurementUnit,
    form=AdminMeasurementUnitForm,
    extra=1,
    can_delete=True,
)


class AdminServiceForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Назва'
    )
    show_in_counters = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label='Показувати в лічильниках'
    )

    unit = forms.ModelChoiceField(
        required=False,
        queryset=MeasurementUnit.objects.all(),
        label='Одиниця вимірювання',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Виберіть...'
    )

    class Meta:
        model = Service
        fields = ['name', 'show_in_counters', 'unit']

AdminServiceFormSet = forms.modelformset_factory(
    model=Service,
    form=AdminServiceForm,
    extra=1,
    can_delete=True,
)