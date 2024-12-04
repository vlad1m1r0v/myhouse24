from django import forms

from src.core.utils import AJAXModelChoiceField
from src.meter_indicators.models import MeterIndicator, StatusChoices
from src.flats.models import Flat
from src.houses.models import HouseSection, House
from src.system_settings.models import Service


class AdminMeterIndicatorForm(forms.ModelForm):
    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        label="Номер показника лічильника")

    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата народження'
    )

    status = forms.ChoiceField(
        choices=StatusChoices.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус')

    house = AJAXModelChoiceField(
        queryset=House.objects.none(),
        label='Будинок',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...',
        required=False
    )

    section = AJAXModelChoiceField(
        queryset=HouseSection.objects.none(),
        label='Секція',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...',
        required=False,
    )

    flat = AJAXModelChoiceField(
        queryset=Flat.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Квартира',
        empty_label='Виберіть...',
        required=False
    )

    service = forms.ModelChoiceField(
        required=False,
        queryset=Service.objects,
        label='Послуга',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Виберіть...'
    )

    value = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0.0, 'step': 0.1}),
        label="Показник рахунку")

    class Meta:
        model = MeterIndicator
        fields = '__all__'
