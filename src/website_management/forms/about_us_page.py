from django import forms
from django.forms import modelformset_factory

from src.website_management.models import AboutUsPage, AboutUsGallery, AboutUsAdditionalGallery, AboutUsDocument


class AdminAboutUsPageForm(forms.ModelForm):
    director_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(),
        label='Рекомендований розмір: (250x310)')

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Заголовок"
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control wysihtml5',
                'rows': 6,
                'style': 'width: 100%;'
            }
        ),
        label='Стислий опис'
    )

    additional_title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Заголовок"
    )

    additional_description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control wysihtml5',
                'rows': 6,
                'style': 'width: 100%;'
            }
        ),
        label='Стислий опис'
    )

    seo_title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="SEO заголовок"
    )

    seo_description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'style': 'resize: none;'
            }
        ),
        label='SEO опис'
    )

    seo_keywords = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'style': 'resize: none;'
            }
        ),
        label='SEO ключові слова'
    )

    class Meta:
        model = AboutUsPage
        fields = '__all__'


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

class AdminAboutUsDocumentForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Назва документу"
    )

    file = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept':'.jpg, .jpeg, .pdf'
            }
        ),
        label='PDF, JPG (макс. розмір 20 Mb)'
    )

    class Meta:
        model = AboutUsDocument
        fields = ['title', 'file']


AdminAboutUsDocumentFormSet = modelformset_factory(
    AboutUsDocument,
    form=AdminAboutUsDocumentForm,
    extra=1,
    can_delete=True
)