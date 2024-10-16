from django import forms
from django.forms import inlineformset_factory

from src.authentication.models import CustomUser
from src.houses.models import House, HouseSection, HouseFloor, HouseUser


class AdminHouseForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'minlength': 5,
                'maxlength': 30
            }
        )
    )

    address = forms.CharField(
        label='Адреса',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'minlength': 10,
                'maxlength': 60
            }
        )
    )

    image_1 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #1. Рекомендований розмір: (522x350)')

    image_2 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #2. Рекомендований розмір: (248x160)')

    image_3 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #3. Рекомендований розмір: (248x160)')

    image_4 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #4. Рекомендований розмір: (248x160)')

    image_5 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #5. Рекомендований розмір: (248x160)')

    class Meta:
        model = House
        fields = '__all__'


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
