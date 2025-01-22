from django import forms
from django.forms import inlineformset_factory

from src.authentication.models import CustomUser
from src.houses.models import House, HouseUser


class AdminHouseUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        required=False,
        queryset=CustomUser.objects.filter(is_staff=True),
        label='ПІБ',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Виберіть...'
    )

    class Meta:
        model = HouseUser
        fields = ['user']


AdminHouseUserFormSet = inlineformset_factory(
    parent_model=House,
    model=HouseUser,
    form=AdminHouseUserForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1
)
