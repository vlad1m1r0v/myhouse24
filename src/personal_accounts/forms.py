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

    def clean_no(self):
        no = self.cleaned_data['no']

        if PersonalAccount.objects.filter(no=no).exists():
            raise ValidationError('Особовий рахунок з таким номером вже існує')

        return no

    def clean_flat(self):
        flat = self.cleaned_data['flat']

        if not flat:
            return

        if self.instance.pk:
            if self.instance.flat == flat:
                return flat

        if Flat.objects.filter(personalaccount__isnull=False, pk=flat.pk).exists():
            raise ValidationError('У квартири, що вказана в формі, вже є особовий рахунок')

        return flat

    def clean(self):
        cleaned_data = super().clean()

        print(cleaned_data)

        if not cleaned_data.get('flat'):
            cleaned_data['house'] = None
            cleaned_data['section'] = None

        return cleaned_data

    class Meta:
        model = PersonalAccount
        fields = '__all__'
