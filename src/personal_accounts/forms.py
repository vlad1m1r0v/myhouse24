from django import forms
from django.core.exceptions import ValidationError

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

    def clean_no(self):
        if PersonalAccount.objects.filter(no=self.cleaned_data['no']).exists():
            raise ValidationError('Особовий рахунок з таким номером вже існує')

    def clean_flat(self):
        if Flat.objects.filter(personalaccount__isnull=False, pk=self.cleaned_data['flat'].pk).exists():
            raise ValidationError('У квартири, що вказана в формі, вже є особовий рахунок')

    class Meta:
        model = PersonalAccount
        fields = '__all__'
