from django import forms
from django.forms import inlineformset_factory

from src.houses.models import House, HouseSection


class AdminHouseSectionForm(forms.ModelForm):
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
        model = HouseSection
        fields = ['name']


AdminHouseSectionFormSet = inlineformset_factory(
    parent_model=House,
    model=HouseSection,
    form=AdminHouseSectionForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1
)