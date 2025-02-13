from django import forms
from django.core.exceptions import ValidationError

from src.meter_indicators.models import MeterIndicator, StatusChoices
from src.flats.models import Flat
from src.houses.models import HouseSection, House
from src.system_settings.models import Service


class AdminMeterIndicatorForm(forms.ModelForm):
    class Meta:
        model = MeterIndicator
        fields = [
            'no',
            'date',
            'status',
            'house',
            'section',
            'flat',
            'service',
            'value',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['house'].widget.choices = [(instance.house.id, str(instance.house))]
            self.fields['section'].widget.choices = [(instance.section.id, str(instance.section))]
            self.fields['flat'].widget.choices = [(instance.flat.id, str(instance.flat))]

    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        label="Номер показника лічильника"
    )

    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата народження'
    )

    status = forms.ChoiceField(
        choices=StatusChoices.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )

    house = forms.CharField(
        label='Будинок',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        required=False
    )

    section = forms.CharField(
        label='Секція',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        required=False,
    )

    flat = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Квартира',
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
        label="Показник рахунку"
    )

    def clean_house(self):
        try:
            return House.objects.get(id=self.cleaned_data['house'])
        except House.DoesNotExist:
            raise ValidationError('Вибраного будинку не знайдено')

    def clean_section(self):
        try:
            return HouseSection.objects.get(id=self.cleaned_data['section'])
        except HouseSection.DoesNotExist:
            raise ValidationError('Вибраної секції не знайдено')

    def clean_flat(self):
        try:
            return Flat.objects.get(id=self.cleaned_data['section'])
        except Flat.DoesNotExist:
            raise ValidationError('Вибраної квартири не знайдено')
