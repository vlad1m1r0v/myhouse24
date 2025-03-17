from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .mixin import FlatOwnerPermissionRequiredMixin
from ...forms import AdminFlatOwnerForm


class AdminFlatOwnerCreateView(SuccessMessageMixin,
                               FlatOwnerPermissionRequiredMixin,
                               CreateView):
    template_name = 'flat_owners/adminlte/create.html'
    form_class = AdminFlatOwnerForm
    success_url = reverse_lazy('adminlte:flat-owners:list')
    success_message = 'Новий власник квартири успішно створений'