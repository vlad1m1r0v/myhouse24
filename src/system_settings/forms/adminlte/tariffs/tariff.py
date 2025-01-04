from django import forms

from src.system_settings.models import Tariff


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