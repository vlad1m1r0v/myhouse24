from django import forms
from django.forms import widgets


class AdminFlatOwnersInvitationForm(forms.Form):
    email = forms.CharField(
        widget=widgets.EmailInput(attrs={"class": "form-control"}),
        label='Електрона пошта'
    )