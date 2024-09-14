from django import forms
from django.forms import modelformset_factory

from src.website_management.models import MainPageSlide, MainPage, MainPageBlock


class AdminMainPageSlideForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Рекомендований розмір: (1920x800)')

    class Meta:
        model = MainPageSlide
        fields = ['image']


AdminMainPageSlideFormSet = modelformset_factory(
    MainPageSlide,
    form=AdminMainPageSlideForm,
    max_num=3,
    extra=3
)


class AdminMainPageForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Заголовок"
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control wysihtml5',
                'rows': 6,
                'style': 'width: 100%;'
            }
        ),
        label='Стислий опис'
    )

    show_app_links = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="Показувати посилання на мобільні додатки"
    )

    seo_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="SEO заголовок"
    )

    seo_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
            }
        ),
        label='SEO опис'
    )

    seo_keywords = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
            }
        ),
        label='SEO ключові слова'
    )

    class Meta:
        model = MainPage
        fields = '__all__'


class AdminMainPageBlockForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Рекомендований розмір: (1000x600)')

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Заголовок блоку"
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control wysihtml5',
                'rows': 6,
                'style': 'width: 100%;'
            }
        ),
        label='Опис'
    )

    class Meta:
        model = MainPageBlock
        fields = ('image', 'title', 'description')


AdminMainPageBlockFormSet = modelformset_factory(
    MainPageBlock,
    form=AdminMainPageBlockForm,
    max_num=6,
    extra=6
)
