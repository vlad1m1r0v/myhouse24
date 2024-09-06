from django import forms
from src.system_settings.models import PaymentCredential


class AdminPaymentCredentialForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Назва компанії')
    information = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 4,
                   'style': 'resize: none;'
                   }),
        label='Інформація')

    class Meta:
        model = PaymentCredential
        fields = ('name', 'information')
