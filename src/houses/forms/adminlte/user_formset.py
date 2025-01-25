from django import forms
from django.forms import inlineformset_factory

from src.core.utils.forms import CustomChoiceField
from src.houses.models import House, HouseUser


class AdminHouseUserForm(forms.ModelForm):
    user = CustomChoiceField(
        required=False,
        label='ПІБ',
        widget=forms.Select(attrs={'class': 'form-control'}),
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
