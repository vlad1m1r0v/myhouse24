from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from src.authentication.models import CustomUser
from src.flats.models import Flat
from src.houses.models import House, HouseSection, HouseFloor
from src.personal_accounts.models import PersonalAccount
from src.system_settings.models import Tariff


class AdminFlatForm(forms.ModelForm):
    class Meta:
        model = Flat

        fields = [
            'no',
            'area',
            'house',
            'section',
            'floor',
            'owner',
            'tariff',
            'personal_account',
        ]

    def __init__(self, *args, **kwargs):
        flat_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if flat_instance:
            personal_account = PersonalAccount.objects.get(flat=flat_instance)
            self.fields['personal_account'].initial = personal_account
            self.fields['personal_account'].queryset = PersonalAccount.objects.filter(
                Q(flat__isnull=True) | Q(flat=flat_instance)
            )
        else:
            self.fields['personal_account'].queryset = PersonalAccount.objects.filter(flat__isnull=True)

    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        label="Номер квартири")

    area = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Площа квартири")

    house = forms.CharField(
        label='Будинок',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    section = forms.CharField(
        label='Секція',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    floor = forms.CharField(
        label='Поверх',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    owner = forms.CharField(
        required=False,
        label='Власник',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    tariff = forms.CharField(
        label='Тариф',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    new_personal_account = forms.CharField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Введіть особовий рахунок',
    )

    personal_account = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=None,
        label='Або виберіть існуючий',
        empty_label='Виберіть...',
    )

    def clean_owner(self):
        try:
            return CustomUser.objects.get(id=self.cleaned_data['owner'])
        except CustomUser.DoesNotExist:
            raise ValidationError('Вибраного користувача не знайдено')

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

    def clean_floor(self):
        try:
            return HouseFloor.objects.get(id=self.cleaned_data['floor'])
        except HouseFloor.DoesNotExist:
            raise ValidationError('Вибраного поверху не знайдено')

    def clean_tariff(self):
        try:
            return Tariff.objects.get(id=self.cleaned_data['tariff'])
        except Tariff.DoesNotExist:
            raise ValidationError('Вибраного тарифу не знайдено')

    def clean(self):
        cleaned_data = super().clean()
        no = cleaned_data.get('new_personal_account')

        if no:
            if self.instance.pk:
                exists = PersonalAccount.objects.filter(no=no).exclude(flat=self.instance).exists()
            else:
                exists = PersonalAccount.objects.filter(no=no).exists()
            if exists:
                raise ValidationError(f'Особовий рахунок з номером {no} вже існує')

        return cleaned_data
