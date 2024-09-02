from cProfile import label

from django import forms

from src.system_settings.models import PaymentItem, TYPE_CHOICES, PaymentCredential


class AdminPaymentItemForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип платежу')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Назва')

    class Meta:
        model = PaymentItem
        fields = ('name', 'type')


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
