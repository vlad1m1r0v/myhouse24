from django import forms

from src.payment_receipts.models import ReceiptTemplate


class AdminReceiptTemplateSelectForm(forms.Form):
    template = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=ReceiptTemplate.objects.all(),
    )