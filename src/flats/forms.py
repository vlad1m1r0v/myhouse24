from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from src.authentication.models import CustomUser
from src.flats.models import Flat
from src.houses.models import House, HouseSection, HouseFloor
from src.personal_accounts.models import PersonalAccount
from src.system_settings.models import Tariff


class AJAXModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            model = self.queryset.model
            value = model.objects.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError("Вибране значення не знайдено в базі даних")
        return value


class AdminFlatForm(forms.ModelForm):
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
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Номер квартири")

    area = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Площа квартири")

    house = AJAXModelChoiceField(
        queryset=House.objects.none(),
        label='Будинок',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...'
    )

    section = AJAXModelChoiceField(
        queryset=HouseSection.objects.none(),
        label='Секція',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...'
    )

    floor = AJAXModelChoiceField(
        queryset=HouseFloor.objects.none(),
        label='Поверх',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...'
    )

    owner = AJAXModelChoiceField(
        required=False,
        queryset=CustomUser.objects.none(),
        label='Власник',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...'
    )

    tariff = AJAXModelChoiceField(
        queryset=Tariff.objects.none(),
        label='Тариф',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        empty_label='Виберіть...'
    )

    new_personal_account = forms.CharField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Особовий рахунок',
    )

    personal_account = forms.ModelChoiceField(
        required=False,
        queryset=None
    )

    def clean(self):
        no = self.cleaned_data.get('new_personal_account')
        if PersonalAccount.objects.filter(no=no).exclude(flat=self.instance).exists():
            raise ValidationError(f'Особовий рахунок з номером {no} вже існує')

    class Meta:
        model = Flat
        fields = '__all__'
