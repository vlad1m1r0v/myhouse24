from django import forms
from django.forms import modelformset_factory

from ...models import AboutUsGallery, AboutUsAdditionalGallery


class AdminAboutUsGalleryForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(),
        label='Рекомендований розмір: (1200x1200)')

    class Meta:
        model = AboutUsGallery
        fields = ['image']

AdminAboutUsGalleryFormSet = modelformset_factory(
    AboutUsGallery,
    form=AdminAboutUsGalleryForm,
    extra=1,
    can_delete=True
)

class AdminAboutUsAdditionalGalleryForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(),
        label='Рекомендований розмір: (1200x1200)')

    class Meta:
        model = AboutUsAdditionalGallery
        fields = ['image']


AdminAboutUsAdditionalGalleryFormSet = modelformset_factory(
    AboutUsAdditionalGallery,
    form=AdminAboutUsAdditionalGalleryForm,
    extra=1,
    can_delete=True
)