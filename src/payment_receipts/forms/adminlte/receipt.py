from django import forms
from django.core.exceptions import ValidationError

from src.payment_receipts.models import (
    Receipt,
    STATUS_CHOICES
)
from src.flats.models import Flat
from src.houses.models import HouseSection, House
from src.personal_accounts.models import PersonalAccount
from src.system_settings.models import Tariff


class AdminReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = [
            'no',
            'date',
            'house',
            'section',
            'flat',
            'is_complete',
            'status',
            'tariff',
            'period_from',
            'period_to',
            'personal_account'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})

        super().__init__(*args, **kwargs)

        house = instance.house if instance else initial.get('house')
        section = instance.section if instance else initial.get('section')
        flat = instance.flat if instance else initial.get('flat')

        if house:
            self.fields['house'].widget.choices = [(house.id, str(house))]

        if section:
            self.fields['section'].widget.choices = [(section.id, str(section))]

        if flat:
            self.fields['flat'].widget.choices = [(flat.id, str(flat))]

    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    )

    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control date'}, format='%d.%m.%Y'),
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

    is_complete = forms.BooleanField(
        label='Проведена',
        widget=forms.CheckboxInput(attrs={'checked': True}),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )

    tariff = forms.CharField(
        label='Тариф',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    period_from = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control date'}, format='%d.%m.%Y'),
        label='Період з'
    )

    period_to = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control date'}, format='%d.%m.%Y'),
        label='Період по'
    )

    personal_account = forms.CharField(
        label='Особовий рахунок',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
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

    def clean_tariff(self):
        try:
            return Tariff.objects.get(id=self.cleaned_data['tariff'])
        except Tariff.DoesNotExist:
            raise ValidationError('Вибраного тарифу не знайдено')

    def clean_personal_account(self):
        try:
            account = PersonalAccount.objects.get(no=self.cleaned_data['personal_account'])

            if account.status == 'disabled':
                raise ValidationError('Не можна оформити квитанцію на відключений особовий рахунок')

            return account

        except PersonalAccount.DoesNotExist:
            raise ValidationError('Вибраного особового рахунку не знайдено')
