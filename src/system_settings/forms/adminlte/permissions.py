from django import forms
from django.contrib.auth.models import Group, Permission
from django.forms import formset_factory

class AdminGroupPermissionForm(forms.Form):
    checkbox = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    permission_id = forms.IntegerField(widget=forms.HiddenInput())
    group_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['checkbox'].initial = self.initial.get('id') is not None

    def save(self):
        group_id = self.cleaned_data['group_id']
        permission_id = self.cleaned_data['permission_id']
        checked = self.cleaned_data['checkbox']

        group = Group.objects.get(id=group_id)
        permission = Permission.objects.get(id=permission_id)

        if checked:
            group.permissions.add(permission)
        else:
            group.permissions.remove(permission)


AdminGroupPermissionFormSet = formset_factory(form=AdminGroupPermissionForm, extra=0)
