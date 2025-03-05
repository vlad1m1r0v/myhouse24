from django import forms
from django.forms import widgets


class AdminCashBoxFiltersForm(forms.Form):
    no = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    date = forms.CharField(
        widget=widgets.Input(attrs={"class": "form-control"})
    )

    status = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
        choices=[
            ('', 'Виберіть...'),
            ('True', 'Проведена'),
            ('False', 'Не проведена'),
        ]
    )

    payment_item = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"})
    )

    owner = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"})
    )

    personal_account = forms.CharField(
        widget=widgets.NumberInput(attrs={"class": "form-control"})
    )

    type = forms.ChoiceField(
        widget=widgets.Select(attrs={"class": "form-control"}),
        choices=[
            ('', 'Виберіть...'),
            ('expense', 'Витрата'),
            ('income', 'Прихід'),
        ]
    )
