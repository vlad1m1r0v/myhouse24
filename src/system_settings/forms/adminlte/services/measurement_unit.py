from django import forms

from src.system_settings.models import MeasurementUnit


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