from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .mixin import (
    MasterCallRequestPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminMasterCallRequestForm
from ...models import MasterCallRequest


class AdminMasterCallRequestCreateView(
    SuccessMessageMixin,
    MasterCallRequestPermissionRequiredMixin,
    HouseUserRequiredMixin,
    CreateView):
    success_message = 'Заявку виклику майстра успішно створено'
    # TODO: change to master call requests list page
    success_url = reverse_lazy('adminlte:master-call-requests:create')
    model = MasterCallRequest
    form_class = AdminMasterCallRequestForm
    template_name = 'master_call_requests/adminlte/create.html'
