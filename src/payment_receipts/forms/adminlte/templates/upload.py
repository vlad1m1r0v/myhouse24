import os
from django import forms
from django.core.exceptions import ValidationError

from src.payment_receipts.models import ReceiptTemplate


def validate_xlsx_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Завантажений файл не має розширення .xlsx')


class AdminReceiptTemplateUploadForm(forms.ModelForm):
    file = forms.FileField(
        validators=[validate_xlsx_extension],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'
        }),
        label='Завантажити користувацький шаблон'
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='Назва'
    )

    class Meta:
        model = ReceiptTemplate
        fields = ['title', 'file']
