from django import forms

from src.personal_accounts.models import STATUS_CHOICES
from src.core.utils import AJAXModelChoiceField
from src.flats.models import Flat
from src.houses.models import HouseSection, House
from src.personal_accounts.models import PersonalAccount


class AdminPersonalAccountForm(forms.ModelForm):
    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        label="Номер особового рахунку")

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус')

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

    flat = AJAXModelChoiceField(
        queryset=Flat.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Квартира',
        empty_label='Виберіть...'
    )

    class Meta:
        model = PersonalAccount
        fields = '__all__'