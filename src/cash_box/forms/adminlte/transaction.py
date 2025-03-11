from django import forms
from django.core.exceptions import ValidationError

from src.authentication.models import CustomUser
from src.cash_box.models import Transaction, TypeChoices
from src.personal_accounts.models import PersonalAccount
from src.system_settings.models import PaymentItem


class AdminTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'no',
            'date',
            'type',
            'owner',
            'personal_account',
            'payment_item',
            'amount',
            'is_complete',
            'manager',
            'comment'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})

        super().__init__(*args, **kwargs)

        owner = instance.owner if instance else initial.get('owner')
        personal_account = instance.personal_account if instance else initial.get('personal_account')
        payment_item = instance.payment_item if instance else initial.get('payment_item')
        manager = instance.manager if instance else initial.get('manager')

        if owner:
            self.fields['owner'].widget.choices = [(owner.id, str(owner))]

        if personal_account:
            self.fields['personal_account'].widget.choices = [(personal_account.id, str(personal_account))]

        if payment_item:
            self.fields['payment_item'].widget.choices = [(payment_item.id, str(payment_item))]

        if manager:
            self.fields['manager'].widget.choices = [(manager.id, str(manager))]

    no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    )

    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d.%m.%Y'),
    )

    type = forms.ChoiceField(
        choices=TypeChoices.choices,
        widget=forms.Select(attrs={'style': 'display: none'}),
    )

    owner = forms.CharField(
        label='Власник квартири',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        required=False,
    )

    personal_account = forms.CharField(
        label='Особовий рахунок',
        widget=forms.Select(attrs={'class': 'form-control select'}),
        required=False,
    )

    payment_item = forms.CharField(
        label='Стаття',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    amount = forms.CharField(
        label='Сума',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1, 'min': 0}),
    )

    is_complete = forms.BooleanField(
        label='Проведена',
        widget=forms.CheckboxInput(attrs={'checked': True}),
        required=False,
    )

    manager = forms.CharField(
        label='Менеджер',
        widget=forms.Select(attrs={'class': 'form-control select'}),
    )

    comment = forms.CharField(
        label='Коментар',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'width: 100%; resize:none'}),
    )

    def clean_owner(self):
        owner = self.cleaned_data['owner']

        if not owner:
            return

        try:
            return CustomUser.objects.get(id=owner)
        except CustomUser.DoesNotExist:
            raise ValidationError('Вибраного власника квартири не знайдено')

    def clean_personal_account(self):
        account = self.cleaned_data['personal_account']

        if not account:
            return

        try:
            account = PersonalAccount.objects.get(id=account)

            if account.status == 'disabled':
                raise ValidationError('Не можна оформити квитанцію на відключений особовий рахунок')

            return account

        except PersonalAccount.DoesNotExist:
            raise ValidationError('Вибраного особового рахунку не знайдено')

    def clean_payment_item(self):
        try:
            return PaymentItem.objects.get(id=self.cleaned_data['payment_item'])
        except PaymentItem.DoesNotExist:
            raise ValidationError('Вибрану статтю платежу квартири не знайдено')

    def clean_manager(self):
        try:
            return CustomUser.objects.get(id=self.cleaned_data['manager'])
        except CustomUser.DoesNotExist:
            raise ValidationError('Вибраного менеджера не знайдено')
