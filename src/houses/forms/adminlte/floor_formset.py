from django import forms
from django.forms import inlineformset_factory

from src.houses.models import House, HouseFloor

class AdminHouseFloorForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        label='Назва',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'minlength': 5,
                'maxlength': 30
            })
    )

    class Meta:
        model = HouseFloor
        fields = ['name']


AdminHouseFloorFormSet = inlineformset_factory(
    parent_model=House,
    model=HouseFloor,
    form=AdminHouseFloorForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1
)
