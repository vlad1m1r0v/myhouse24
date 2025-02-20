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
        initial = kwargs.get('initial', {})

        super().__init__(*args, **kwargs)

        house = instance.house if instance else initial.get('house')
        section = instance.section if instance else initial.get('section')
        flat = instance.flat if instance else initial.get('flat')
        service = instance.service if instance else initial.get('service')

        if house:
            self.fields['house'].widget.choices = [(house.id, str(house))]
        if section:
            self.fields['section'].widget.choices = [(section.id, str(section))]
        if flat:
            self.fields['flat'].widget.choices = [(flat.id, str(flat))]
        if service:
            self.fields['service'].widget.choices = [(service.id, str(service))]

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
    )

    section = forms.CharField(
        label='Секція',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    flat = forms.CharField(
        label='Квартира',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    service = forms.CharField(
        label='Послуга',
        widget=forms.Select(attrs={'class': 'form-control select'}),
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
            return Flat.objects.get(id=self.cleaned_data['flat'])
        except Flat.DoesNotExist:
            raise ValidationError('Вибраної квартири не знайдено')

    def clean_service(self):
        try:
            return Service.objects.get(id=self.cleaned_data['service'])
        except Service.DoesNotExist:
            raise ValidationError('Вибраної послуги не знайдено')
