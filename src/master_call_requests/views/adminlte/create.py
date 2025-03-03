from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .mixin import MasterCallRequestPermissionRequiredMixin
from ...forms import AdminMasterCallRequestForm
from ...models import MasterCallRequest


class AdminMasterCallRequestCreateView(
    SuccessMessageMixin,
    MasterCallRequestPermissionRequiredMixin,
    CreateView):
    success_message = 'Заявку виклику майстра успішно створено'
    success_url = reverse_lazy('adminlte:master-call-requests:list')
    model = MasterCallRequest
    form_class = AdminMasterCallRequestForm
    template_name = 'master_call_requests/adminlte/create.html'
