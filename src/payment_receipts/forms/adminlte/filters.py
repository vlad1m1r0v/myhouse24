from django import forms
from src.payment_receipts.models import STATUS_CHOICES


class AdminReceiptFiltersForm(forms.Form):
    no = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'})
    )

    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
        choices=STATUS_CHOICES + [('', 'Виберіть...')]
    )

    date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'})
    )

    month = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'})
    )

    flat = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'})
    )

    owner = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
    )

    is_complete = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
        choices=[
            ('true', 'Проведена'),
            ('false', 'Не проведена'),
            ('', 'Виберіть...')
        ]
    )
