from django.views.generic import TemplateView

from src.flat_owners.models.flat_owner import FlatOwner
from src.flats.models import Flat
from src.houses.models import House
from src.master_call_requests.models import MasterCallRequest
from src.personal_accounts.models import PersonalAccount
from .mixin import (
    AdminBalanceMixin,
    StatisticsPermissionRequiredMixin
)


class AdminDashboardView(
    AdminBalanceMixin,
    StatisticsPermissionRequiredMixin,
    TemplateView,
):
    template_name = 'dashboard/adminlte/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        houses = House.objects.all()

        if not self.request.user.is_superuser:
            houses = houses.filter(users__user=self.request.user)

        owners = FlatOwner.objects.filter(is_superuser=False, is_staff=False, status='active')

        if not self.request.user.is_superuser:
            owners = owners.filter(flats__house__users__user=self.request.user)

        master_call_requests = MasterCallRequest.objects.all()
        new_master_call_requests = master_call_requests.filter(status='new')

        if not self.request.user.is_superuser:
            master_call_requests = master_call_requests.filter(flat__house__users__user=self.request.user)
            new_master_call_requests = new_master_call_requests.filter(flat__house__users__user=self.request.user)

        flats = Flat.objects.all()

        if not self.request.user.is_superuser:
            flats = owners.filter(house__users__user=self.request.user)

        personal_accounts = PersonalAccount.objects.all()

        if not self.request.user.is_superuser:
            personal_accounts = personal_accounts.filter(house__users__user=self.request.user)

        context['houses'] = houses.count()
        context['owners'] = owners.count()
        context['master_call_requests'] = master_call_requests.count()
        context['flats'] = flats.count()
        context['personal_accounts'] = personal_accounts.count()
        context['new_master_call_requests'] = new_master_call_requests.count()

        return context
