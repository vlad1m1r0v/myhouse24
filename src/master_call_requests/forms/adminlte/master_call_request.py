from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from src.master_call_requests.models import (
    MasterCallRequest,
    StatusChoices
)
from src.flats.models import Flat
from src.authentication.models import CustomUser


class FlatOwnerSelect(forms.Select):
    def __init__(self, *args, initial_phone, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control select"

        super().__init__(*args, **kwargs)
        self.initial_phone = initial_phone

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)

        option["attrs"]["class"] = "form-control select"
        option["attrs"]["data-phone"] = self.initial_phone

        return option


class FlatSelect(forms.Select):
    def __init__(self, *args, initial_house_id, initial_house_name, initial_section_name, initial_floor_name, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control select"

        super().__init__(*args, **kwargs)

        self.initial_house_id = initial_house_id
        self.initial_house_name = initial_house_name
        self.initial_section_name = initial_section_name
        self.initial_floor_name = initial_floor_name

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)

        option["attrs"]["data-house-id"] = self.initial_house_id
        option["attrs"]["data-house-name"] = self.initial_house_name
        option["attrs"]["data-section-name"] = self.initial_section_name
        option["attrs"]["data-floor-name"] = self.initial_floor_name

        return option


class AdminMasterCallRequestForm(forms.ModelForm):
    class Meta:
        model = MasterCallRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        super().__init__(*args, **kwargs)

        if instance:
            flat_owner = instance.flat_owner
            flat = instance.flat
            master = instance.master

            self.fields['flat_owner'].widget = FlatOwnerSelect(initial_phone=flat_owner.phone_number)
            self.fields['flat_owner'].widget.choices = [(flat_owner.id, str(flat_owner))]

            self.fields['flat'].widget = FlatSelect(
                initial_house_id=flat.house_id,
                initial_house_name=flat.house.name,
                initial_section_name=flat.section.name,
                initial_floor_name=flat.floor.name,
            )
            self.fields['flat'].widget.choices = [(flat.id, str(flat))]

            if master:
                self.fields['master'].widget.choices = [(master.id, str(master))]

    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата'
    )

    time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    flat_owner = forms.CharField(
        label='Власник',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control select', 'rows': 5, 'style': 'resize:none;'}),
        label='Опис'
    )

    flat = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Квартира',
    )

    master_type = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Сантехнік', 'Електрик']),
        label='Тип майстра',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Будь-який спеціаліст',
        required=False
    )

    status = forms.ChoiceField(
        choices=StatusChoices.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )

    master = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Майстер',
        required=False,
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'width: 100%;'}),
        label='Коментарій'
    )

    def clean_flat_owner(self):
        try:
            return CustomUser.objects.get(id=self.cleaned_data['flat_owner'])
        except CustomUser.DoesNotExist:
            raise ValidationError('Вибраного власника не знайдено')

    def clean_flat(self):
        try:
            return Flat.objects.get(id=self.cleaned_data['flat'])
        except Flat.DoesNotExist:
            raise ValidationError('Вибраної квартири не знайдено')

    def clean_master(self):
        master = self.cleaned_data['master']

        if not master:
            return

        try:
            return CustomUser.objects.get(id=master)
        except CustomUser.DoesNotExist:
            raise ValidationError('Вибраного майстра не знайдено')
