from django import forms

from src.system_settings.models import Service, MeasurementUnit


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

    class Meta:
        model = Service
        fields = ['name', 'show_in_counters', 'unit']

        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'unit': 'Одиниця вимірювання',
        }

    def __init__(self, *args, **kwargs):
        unit_choices = kwargs.pop('unit_choices', [])

        super(AdminServiceForm, self).__init__(*args, **kwargs)

        self.fields['unit'].choices = unit_choices

    def clean(self):
        unit = self.cleaned_data.get('unit')
        name = self.cleaned_data.get('name')

        if bool(unit) != bool(name):
            raise forms.ValidationError('Не вказано назву або одиницю вимірювання')
        elif name and len(name) < 5:
            raise forms.ValidationError("Назва послуги має містити хоча б 5 символів")


class BaseAdminServiceFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = MeasurementUnit.objects

        self.unit_choices = [*forms.ModelChoiceField(
            queryset=qs,
            empty_label='Виберіть...',
        ).choices]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['unit_choices'] = self.unit_choices
        return kwargs


AdminServiceFormSet = forms.modelformset_factory(
    model=Service,
    form=AdminServiceForm,
    formset=BaseAdminServiceFormSet,
    extra=1,
    can_delete=True,
)
