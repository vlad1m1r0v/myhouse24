from django import forms
from django.forms import modelformset_factory

from ...models import TariffsPageBlock


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