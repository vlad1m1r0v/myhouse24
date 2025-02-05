from django import forms
from django.contrib.auth.models import Group
from django.db.models import OuterRef, Subquery
from django.forms import inlineformset_factory, BaseInlineFormSet

from src.authentication.models import CustomUser, STATUS_CHOICES
from src.houses.models import House, HouseUser


class UserSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-role"] = value.instance.role
        return option


class AdminHouseUserForm(forms.ModelForm):
    class Meta:
        model = HouseUser

        widgets = {
            'user': UserSelect(attrs={'class': 'form-control'}),
        }

        labels = {
            'user': 'Прізвище Ім\'я',
        }

        fields = ['user']

    def __init__(self, *args, **kwargs):
        user_choices = kwargs.pop('user_choices', [])

        super(AdminHouseUserForm, self).__init__(*args, **kwargs)

        self.fields['user'].choices = user_choices


class BaseAdminHouseUserFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        role_subquery = Subquery(Group.objects.filter(user=OuterRef('pk')).order_by('id')[:1].values('name'))
        qs = CustomUser.objects.filter(is_staff=True, status="active").annotate(role=role_subquery)

        self.user_choices = [*forms.ModelChoiceField(
            queryset=qs,
            empty_label='Виберіть...',
        ).choices]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['user_choices'] = self.user_choices
        return kwargs


AdminHouseUserFormSet = inlineformset_factory(
    parent_model=House,
    model=HouseUser,
    form=AdminHouseUserForm,
    formset=BaseAdminHouseUserFormSet,
    can_delete=True,
    can_delete_extra=True,
    extra=1
)
