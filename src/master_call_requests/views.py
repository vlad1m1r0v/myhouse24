from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Value, F, CharField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from src.authentication.models import CustomUser
from src.core.utils import is_ajax
from src.flats.models import Flat
from src.master_call_requests.forms import AdminMasterCallRequestForm
from src.master_call_requests.models import MasterCallRequest


# Create your views here.
class MasterCallRequestPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.service_call_requests'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до викликів майстрів'})
            else:
                messages.error(request, 'У Вас немає доступу до викликів майстрів')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


class AdminMasterCallRequestFlatView(
    MasterCallRequestPermissionRequiredMixin,
    View):
    def get(self, request, *args, **kwargs):
        flat_id = kwargs.get('flat_id')
        detail = Flat.objects.values('house_id', 'house__name', 'floor__name').get(pk=flat_id)
        return JsonResponse(data=detail, safe=False)


class AdminMasterCallRequestMastersView(
    MasterCallRequestPermissionRequiredMixin,
    View):
    def get(self, request, *args, **kwargs):
        group_id = request.GET.get('group_id')

        if group_id:
            masters = CustomUser.objects.filter(groups__id=group_id)
        else:
            masters = CustomUser.objects.filter(groups__name__in=['Сантехнік', 'Електрик'])

        masters = masters.annotate(
            annotated_field=Concat(
                F('first_name'),
                Value(' '),
                F('last_name'),
                Value(' - '),
                F('groups__name'),
                output_field=CharField()
            )
        ).values('id', 'annotated_field')

        return JsonResponse(data=list(masters), safe=False)


class AdminMasterCallRequestCreateView(
    SuccessMessageMixin,
    MasterCallRequestPermissionRequiredMixin,
    CreateView):
    success_message = 'Нову заявка виклику майстра успішно створено'
    # TODO: change to master call requests list page
    success_url = reverse_lazy('adminlte_master_call_request_create')
    form_class = AdminMasterCallRequestForm
    template_name = 'create_master_call_request.html'


class AdminMasterCallRequestUpdateView(
    SuccessMessageMixin,
    MasterCallRequestPermissionRequiredMixin,
    UpdateView):
    success_message = 'Заявку виклику майстра успішно оновлено'
    # TODO: change to master call requests list page
    success_url = reverse_lazy('adminlte_master_call_request_create')
    model = MasterCallRequest
    form_class = AdminMasterCallRequestForm
    template_name = 'update_master_call_request.html'
