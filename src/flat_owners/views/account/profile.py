from django.views.generic import TemplateView
from src.core.utils.permissions import OwnerRequiredMixin


class AccountProfileView(
    OwnerRequiredMixin,
    TemplateView
):
    template_name = 'flat_owners/account/profile.html'
