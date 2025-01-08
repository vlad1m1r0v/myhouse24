from django import forms
from django.forms import modelformset_factory

from ...models import MainPageSlide


class AdminMainPageSlideForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(),
        label='Рекомендований розмір: (1920x800)')

    class Meta:
        model = MainPageSlide
        fields = ['image']


AdminMainPageSlideFormSet = modelformset_factory(
    MainPageSlide,
    form=AdminMainPageSlideForm,
    max_num=3,
    extra=3
)