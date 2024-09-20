from django import forms
from django.forms import modelformset_factory

from src.website_management.models import TariffsPage, TariffsPageBlock

class AdminTariffsPageForm(forms.ModelForm):
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
        model = TariffsPage
        fields = '__all__'


class AdminTariffsPageBlockForm(forms.ModelForm):
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
        label="Підпис"
    )

    def clean(self):
        image = bool(self.cleaned_data.get('image'))
        title = bool(self.cleaned_data.get('title'))

        if any([image, title]) and not all([image, title]):
            raise forms.ValidationError("Для тарифу не вибране зображення або не вказана назва")


    class Meta:
        model = TariffsPageBlock
        fields = ('image', 'title')


AdminTariffsPageBlockFormSet = modelformset_factory(
    TariffsPageBlock,
    form=AdminTariffsPageBlockForm,
    extra=1,
    can_delete=True,
)