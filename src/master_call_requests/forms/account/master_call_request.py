from django import forms
from django.contrib.auth.models import Group

from src.flats.models import Flat
from src.master_call_requests.models import MasterCallRequest


class AccountMasterCallRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        self.user = user

        self.fields['flat'].queryset = Flat.objects.select_related('house').filter(owner=self.user)
        self.fields['flat'].label_from_instance_ = self.flat_label

    master_type = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Сантехнік', 'Електрик']),
        label='Тип майстра',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Будь-який спеціаліст',
        required=False
    )

    flat = forms.ModelChoiceField(
        queryset=Flat.objects.none(),
        label='Квартира',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Виберіть...'
    )

    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
        label='Дата'
    )

    time = forms.TimeField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Час'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control select', 'rows': 5, 'style': 'resize:none;'}),
        label='Опис'
    )

    @staticmethod
    def flat_label(self, flat):
        return f"{flat.house.name}, кв. № {flat.no}"

    class Meta:
        model = MasterCallRequest
        fields = [
            'master_type',
            'flat',
            'date',
            'time',
            'description'
        ]