from django import forms
from django.forms import modelformset_factory

from src.website_management.models import MainPageBlock


class AdminMainPageBlockForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(),
        label='Рекомендований розмір: (1000x600)')

    title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Заголовок блоку"
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
        label='Опис'
    )

    def clean(self):
        image = bool(self.cleaned_data.get('image'))
        title = bool(self.cleaned_data.get('title'))
        description = bool(self.cleaned_data.get('description'))

        if any([image, title, description]) and not all([image, title, description]):
            raise forms.ValidationError("Для блоку \"Поруч з нами\" не вибране зображення або не вказана назва чи опис")


    class Meta:
        model = MainPageBlock
        fields = ('image', 'title', 'description')


AdminMainPageBlockFormSet = modelformset_factory(
    MainPageBlock,
    form=AdminMainPageBlockForm,
    max_num=6,
    extra=6
)