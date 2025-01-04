from django import forms
from src.system_settings.models import PaymentItem, TYPE_CHOICES


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