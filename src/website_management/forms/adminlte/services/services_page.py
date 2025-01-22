from django import forms

from src.website_management.models import ServicesPage

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