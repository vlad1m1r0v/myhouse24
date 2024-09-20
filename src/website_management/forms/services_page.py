from django import forms
from django.forms import modelformset_factory

from src.website_management.models import ServicesPage, ServicesPageBlock

class AdminServicesPageForm(forms.ModelForm):
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
        model = ServicesPage
        fields = '__all__'


class AdminServicesPageBlockForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Рекомендований розмір: (650x300)')

    title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Назва послуги"
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control wysihtml5',
                'rows': 6,
                'style': 'width: 100%;'
            }
        ),
        label='Опис послуги'
    )

    def clean(self):
        image = bool(self.cleaned_data.get('image'))
        title = bool(self.cleaned_data.get('title'))
        description = bool(self.cleaned_data.get('description'))

        if any([image, title, description]) and not all([image, title, description]):
            raise forms.ValidationError("Для послуги не вибране зображення або не вказана назва чи опис")


    class Meta:
        model = ServicesPageBlock
        fields = ('image', 'title', 'description')


AdminServicesPageBlockFormSet = modelformset_factory(
    ServicesPageBlock,
    form=AdminServicesPageBlockForm,
    extra=1,
    can_delete=True,
)