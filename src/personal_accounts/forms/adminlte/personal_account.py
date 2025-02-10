from django import forms
from django.core.exceptions import ValidationError

from ...models import STATUS_CHOICES
from src.flats.models import Flat
from src.houses.models import HouseSection, House
from src.personal_accounts.models import PersonalAccount


class AdminPersonalAccountForm(forms.ModelForm):
    class Meta:
        model = PersonalAccount
        fields = [
            'no',
            'status',
            'house',
            'section',
            'flat',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['house'].widget.choices = [(instance.house.id, str(instance.house))] if instance.house else []
            self.fields['section'].widget.choices = [
                (instance.section.id, str(instance.section))] if instance.section else []
            self.fields['flat'].widget.choices = [(instance.flat.id, str(instance.flat))] if instance.flat else []

    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        label="Номер особового рахунку")

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус')

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

    def clean_no(self):
        no = self.cleaned_data['no']

        is_current_no = False

        if self.instance:
            is_current_no = str(self.instance.no) == no

        does_account_with_number_exist = PersonalAccount.objects.filter(no=no).exists()

        if is_current_no and does_account_with_number_exist:
            raise ValidationError('Особовий рахунок з таким номером вже існує')

        return no

    def clean_house(self):
        house = self.cleaned_data['house']

        if not house:
            return

        try:
            return House.objects.get(id=house)
        except House.DoesNotExist:
            raise ValidationError('Вибраного будинку не знайдено')

    def clean_section(self):
        section = self.cleaned_data['section']

        if not section:
            return

        try:
            return HouseSection.objects.get(id=section)
        except HouseSection.DoesNotExist:
            raise ValidationError('Вибраної секції не знайдено')

    def clean_flat(self):
        flat = self.cleaned_data['flat']

        if not flat:
            return

        is_current_flat = False

        if self.instance:
            is_current_flat = str(self.instance.flat.id) == flat

        does_flat_have_account = Flat.objects.filter(personalaccount__isnull=False, pk=flat).exists()

        if does_flat_have_account and (not is_current_flat):
            raise ValidationError('У квартири, що вказана в формі, вже є особовий рахунок')

        try:
            return Flat.objects.get(id=flat)
        except Flat.DoesNotExist:
            raise ValidationError('Вибраної квартири не знайдено')

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('flat'):
            cleaned_data['house'] = None
            cleaned_data['section'] = None

        return cleaned_data
