from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from src.core.utils import is_ajax
from src.flats.models import Flat
from src.meter_indicators.forms import AdminMeterIndicatorForm
from src.meter_indicators.models import MeterIndicator
from src.system_settings.models import Service


class MeterIndicatorPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.meter_indicators'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до показників рахунків'})
            else:
                messages.error(request, 'У Вас немає доступу до показників рахунків')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
class AdminCreateMeterIndicatorView(
    SuccessMessageMixin,
    MeterIndicatorPermissionRequiredMixin,
    CreateView):
    template_name = 'create_meter_indicator.html'
    success_message = 'Новий показник рахунку успішно створено'

    def get_form(self, **kwargs):
        flat_id = self.request.GET.get('flat_id', None)
        service_id = self.request.GET.get('service_id', None)

        if flat_id and service_id:
            flat = Flat.objects.select_related('house', 'section').get(pk=flat_id)
            service = Service.objects.get(pk=service_id)

            return AdminMeterIndicatorForm(
                self.request.POST or None,
                initial={
                    'house': flat.house,
                    'section': flat.section,
                    'flat': flat,
                    'service': service
                }
            )

        return AdminMeterIndicatorForm(self.request.POST or None)

    def get_success_url(self):
        if 'save_and_add_new' in self.request.POST:

            form = self.get_form()

            if form.is_valid():

                flat_id = form.cleaned_data.get('flat').id
                service_id = form.cleaned_data.get('service').id

                if flat_id and service_id:
                    sorted_flats = Flat.objects.order_by('house', 'section', 'no')

                    try:
                        current_flat = Flat.objects.get(pk=flat_id)
                        next_flat = sorted_flats.filter(
                            Q(house__gt=current_flat.house) |
                            Q(house=current_flat.house, section__gt=current_flat.section) |
                            Q(house=current_flat.house, section=current_flat.section, no__gt=current_flat.no)
                        ).first()

                        if next_flat:
                            return f"{reverse_lazy('adminlte_meter_indicator_create')}?flat_id={next_flat.id}&service_id={service_id}"
                    except Flat.DoesNotExist:
                        pass

                return reverse_lazy('adminlte_meter_indicator_create')

        # TODO: change to meter indicators list page URL
        return reverse_lazy('adminlte_meter_indicator_create')


class AdminUpdateMeterIndicatorView(
    SuccessMessageMixin,
    MeterIndicatorPermissionRequiredMixin,
    UpdateView):
    model = MeterIndicator
    form_class = AdminMeterIndicatorForm
    template_name = 'update_meter_indicator.html'
    success_message = 'Показник рахунку успішно оновлено'

    def get_success_url(self):
        if 'save_and_add_new' in self.request.POST:

            form = self.get_form()

            if form.is_valid():

                flat_id = form.cleaned_data.get('flat').id
                service_id = form.cleaned_data.get('service').id

                if flat_id and service_id:
                    sorted_flats = Flat.objects.order_by('house', 'section', 'no')

                    try:
                        current_flat = Flat.objects.get(pk=flat_id)
                        next_flat = sorted_flats.filter(
                            Q(house__gt=current_flat.house) |
                            Q(house=current_flat.house, section__gt=current_flat.section) |
                            Q(house=current_flat.house, section=current_flat.section, no__gt=current_flat.no)
                        ).first()

                        if next_flat:
                            return f"{reverse_lazy('adminlte_meter_indicator_create')}?flat_id={next_flat.id}&service_id={service_id}"
                    except Flat.DoesNotExist:
                        pass

                return reverse_lazy('adminlte_meter_indicator_create')

        # TODO: change to meter indicators list page URL
        return reverse_lazy('adminlte_meter_indicator_create')
