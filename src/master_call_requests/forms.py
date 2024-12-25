from django import forms
from django.contrib.auth.models import Group
from django.db.models import Count

from src.authentication.models import CustomUser
from src.core.utils import AJAXModelChoiceField
from src.flats.models import Flat
from src.master_call_requests.models import MasterCallRequest, StatusChoices


class AdminMasterCallRequestForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата народження'
    )

    time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    flat_owner = forms.ModelChoiceField(
        queryset=CustomUser.objects.annotate(flat_count=Count('flat')).filter(
            is_staff=False,
            flat_count__gt=0
        ),
        label='Власник',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Виберіть...'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'resize:none;'}),
        label='Опис'
    )

    flat = AJAXModelChoiceField(
        queryset=Flat.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Квартира',
        empty_label='Виберіть...',
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
        label='Статус')

    master = AJAXModelChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control select'}),
        label='Майстер',
        empty_label='Виберіть...',
        required=False
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'width: 100%;'}),
        label='Коментарій'
    )

    class Meta:
        model = MasterCallRequest
        fields = '__all__'
