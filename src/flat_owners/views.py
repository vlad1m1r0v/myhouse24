from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from src.authentication.models import CustomUser
from src.core.utils import is_ajax
from src.flat_owners.forms import AdminFlatOwnerForm


class FlatOwnerPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.flat_owners'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до власників квартир'})
            else:
                messages.error(request, 'У Вас немає доступу до власників квартир')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


class AdminFlatOwnerCreateView(SuccessMessageMixin,
                               FlatOwnerPermissionRequiredMixin,
                               CreateView):
    template_name = 'flat_owners/create_flat_owner.html'
    form_class = AdminFlatOwnerForm
    # TODO: change to flat owners list page URL
    success_url = reverse_lazy('adminlte_flat_owner_create')
    success_message = 'Новий власник квартири успішно створений'


class AdminFlatOwnerUpdateView(SuccessMessageMixin,
                               FlatOwnerPermissionRequiredMixin,
                               UpdateView):
    model = CustomUser
    template_name = 'flat_owners/update_flat_owner.html'
    form_class = AdminFlatOwnerForm
    # TODO: change to flat owners list page URL
    success_url = reverse_lazy('adminlte_flat_owner_create')
    success_message = 'Дані власника квартири успішно оновлено'
