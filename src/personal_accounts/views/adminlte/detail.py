from django.views.generic import DetailView
from src.personal_accounts.models import PersonalAccount

from .mixin import (
    HouseUserRequiredMixin,
    PersonalAccountPermissionRequiredMixin
)


class AdminPersonalAccountDetailView(
    HouseUserRequiredMixin,
    PersonalAccountPermissionRequiredMixin,
    DetailView
):
    model = PersonalAccount
    context_object_name = 'personal_account'
    template_name = 'personal_accounts/adminlte/detail.html'

    def get_queryset(self):
        return (super()
                .get_queryset()
                .with_balance()
                .select_related("house", "section", "flat", "flat__owner"))
