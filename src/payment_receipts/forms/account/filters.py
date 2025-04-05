from django import forms
from src.payment_receipts.models import STATUS_CHOICES


class AccountReceiptFiltersForm(forms.Form):
    date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'})
    )

    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
        choices=STATUS_CHOICES + [('', 'Виберіть...')]
    )
