from django import forms
from django.forms import modelformset_factory

from src.website_management.models import AboutUsDocument


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