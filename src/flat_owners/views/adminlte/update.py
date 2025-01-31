from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.authentication.models import CustomUser
from .mixin import FlatOwnerPermissionRequiredMixin
from ...forms import AdminFlatOwnerForm


class AdminFlatOwnerUpdateView(SuccessMessageMixin,
                               FlatOwnerPermissionRequiredMixin,
                               UpdateView):
    model = CustomUser
    template_name = 'flat_owners/adminlte/update.html'
    form_class = AdminFlatOwnerForm
    # TODO: change to flat owners list page URL
    success_url = reverse_lazy('adminlte:flat-owners:create')
    success_message = 'Дані власника квартири успішно оновлено'
