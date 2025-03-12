from django import forms
from django.core.exceptions import ValidationError

from src.authentication.models import CustomUser
from src.houses.models import House, HouseSection, HouseFloor
from src.flats.models import Flat
from src.user_messages.models import Message


class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'creator',
            'topic',
            'description',
            'to_debtors',
            'house',
            'section',
            'floor',
            'flat',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})

        super().__init__(*args, **kwargs)

        creator = instance.creator if instance else initial.get('creator')
        house = instance.house if instance else initial.get('house')
        section = instance.section if instance else initial.get('section')
        floor = instance.floor if instance else initial.get('floor')
        flat = instance.flat if instance else initial.get('flat')

        if creator:
            self.fields['creator'].widget.choices = [(creator.id, str(creator))]

        if house:
            self.fields['house'].widget.choices = [(house.id, str(house))]

        if section:
            self.fields['section'].widget.choices = [(section.id, str(section))]

        if floor:
            self.fields['floor'].widget.choices = [(floor.id, str(floor))]

        if flat:
            self.fields['flat'].widget.choices = [(flat.id, str(flat))]

    creator = forms.CharField(
        widget=forms.Select(attrs={'style': 'display:none'}),
    )

    topic = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема повідомлення'}),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'style': 'width: 100%',
                'placeholder': 'Текст повідомлення'}
        ),
    )

    to_debtors = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label='Боржникам'
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

    floor = forms.CharField(
        label='Поверх',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        required=False,
    )

    flat = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Квартира',
        required=False
    )

    def clean_creator(self):
        try:
            return CustomUser.objects.get(id=self.cleaned_data['creator'])
        except CustomUser.DoesNotExist:
            raise ValidationError('Користувача не знайдено')

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

    def clean_floor(self):
        floor = self.cleaned_data['floor']

        if not floor:
            return

        try:
            return HouseFloor.objects.get(id=floor)
        except HouseFloor.DoesNotExist:
            raise ValidationError('Вибраного поверху не знайдено')

    def clean_flat(self):
        flat = self.cleaned_data['flat']

        if not flat:
            return

        try:
            return Flat.objects.get(id=flat)
        except Flat.DoesNotExist:
            raise ValidationError('Вибраної квартири не знайдено')
