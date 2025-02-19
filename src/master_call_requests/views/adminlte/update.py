from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .mixin import (
    MasterCallRequestPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminMasterCallRequestForm
from ...models import MasterCallRequest


class AdminMasterCallRequestUpdateView(
    SuccessMessageMixin,
    HouseUserRequiredMixin,
    MasterCallRequestPermissionRequiredMixin,
    UpdateView):
    success_message = 'Заявку виклику майстра успішно оновлено'
    # TODO: change to master call requests list page
    success_url = reverse_lazy('adminlte:master-call-requests:create')
    model = MasterCallRequest
    form_class = AdminMasterCallRequestForm
    template_name = 'master_call_requests/adminlte/update.html'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'flat_owner',
            'flat',
            'flat__house',
            'flat__section',
            'flat__floor'
        )
