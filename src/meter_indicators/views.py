from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, View
from django.template.defaultfilters import date as _date

from src.core.utils import is_ajax
from src.flats.models import Flat
from src.houses.models import House, HouseSection
from src.meter_indicators.forms import AdminMeterIndicatorForm
from src.meter_indicators.models import MeterIndicator, StatusChoices
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

        initial = {}

        if flat_id:
            flat = Flat.objects.select_related('house', 'section').get(pk=flat_id)

            initial['house'] = flat.house
            initial['section'] = flat.section
            initial['flat'] = flat

            if service_id:
                service = Service.objects.get(pk=service_id)

                initial['service'] = service

            return AdminMeterIndicatorForm(
                self.request.POST or None,
                initial=initial
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

        return reverse_lazy('adminlte_meter_indicators_list')


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

        return reverse_lazy('adminlte_meter_indicators_list')


class AdminDetailMeterIndicatorView(
    MeterIndicatorPermissionRequiredMixin,
    DetailView
):
    model = MeterIndicator
    template_name = 'detail_meter_indicator.html'


class AdminMeterIndicatorForFlatView(
    MeterIndicatorPermissionRequiredMixin,
    TemplateView
):
    template_name = 'list_meter_indicators_for_flat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flat_id = self.request.GET.get('flat_id', None)
        flat = Flat.objects.get(pk=flat_id)
        context["flat"] = flat

        service_id = self.request.GET.get('service_id', None)

        if service_id:
            service = Service.objects.get(pk=service_id)
            context["service"] = service

        return context


class AdminMeterIndicatorsForFlatDatatableView(AjaxDatatableView):
    model = MeterIndicator
    title = 'Показники лічильників'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    initial_order = [[0, 'asc']]

    column_defs = [
        {
            'name': 'pk',
            'visible': False,
            'orderable': True,
        },
        {
            'name': 'no',
            'title': 'Номер',
            'visible': True,
            'orderable': False,
        },
        {
            'name': 'status',
            'title': 'Статус',
            'visible': True,
            'choices': StatusChoices.choices,
            'orderable': False,
        },
        {
            'name': 'date',
            'title': 'Дата',
            'className': 'daterange-filter',
            'visible': True
        },
        {
            'name': 'month',
            'title': 'Місяць',
            'placeholder': True,
            'visible': True,
            'searchable': False,
            'orderable': True,
        },
        {
            'name': 'house__id',
            'title': 'Будинок',
            'className': 'house-filter',
            'visible': True,
            'choices': [(house.id, house.name) for house in House.objects.all()],
            'orderable': False
        },
        {
            'name': 'section__id',
            'title': 'Секція',
            'className': 'section-filter',
            'visible': True,
            'choices': [],
            'orderable': False
        },
        {
            'name': 'flat__id',
            'title': 'Номер квартири',
            'className': 'flat-filter',
            'visible': True,
            'choices': [],
            'orderable': False
        },
        {
            'name': 'service__id',
            'title': 'Послуга',
            'visible': True,
            'choices': [(service.id, service.name) for service in Service.objects.all()],
            'orderable': False
        },
        {
            'name': 'value',
            'title': 'Показник',
            'visible': True,
            'placeholder': True,
            'searchable': False,
            'orderable': False,
        },
        {
            'name': 'service__unit__unit',
            'title': 'Одиниця',
            'visible': True,
            'placeholder': True,
            'searchable': False,
            'orderable': False,
        },
        {
            'name': 'button_group',
            'title': '',
            'placeholder': True, 'visible': True,
            'searchable': False,
            'orderable': False,
        },
    ]

    def get_initial_queryset(self, request=None):
        filters = Q()

        flat_id = self.request.REQUEST.get('flat_id')
        if flat_id:
            filters &= Q(flat__id=flat_id)

        service_id = self.request.REQUEST.get('service_id')
        if service_id:
            filters &= Q(service_id=service_id)

        return MeterIndicator.objects.filter(filters)

    def filter_queryset(self, params, qs):
        for column_link in params['column_links']:
            if column_link.searchable and column_link.search_value:
                if column_link.name == 'date':
                    date_range = column_link.search_value

                    date_start = datetime.strptime(date_range.split(' - ')[0], '%d.%m.%Y')
                    date_end = datetime.strptime(date_range.split(' - ')[1], '%d.%m.%Y')

                    qs = qs.filter(Q(date__gte=date_start), Q(date__lte=date_end))
                else:
                    qs = self.filter_queryset_by_column(column_link.name, column_link.search_value, qs)
        return qs

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'month':
                if order.ascending:
                    return qs.order_by('date')
                return qs.order_by('-date')

            break

        return super().sort_queryset(params, qs)

    def customize_row(self, row, obj):
        if obj.status == 'new':
            row['status'] = f"<small class='label label-warning'>{obj.get_status_display()}</small>"
        if obj.status == 'accounted' or obj.status == 'accounted_paid':
            row['status'] = f"<small class='label label-success'>{obj.get_status_display()}</small>"
        if obj.status == 'zero':
            row['status'] = f"<small class='label label-primary'>{obj.get_status_display()}</small>"

        row['month'] = _date(obj.date, "F")

        row['house__id'] = obj.house.name

        row['section__id'] = obj.section.name

        row['flat__id'] = obj.flat.no

        row['service__id'] = obj.service.name

        row['service__unit__unit'] = obj.service.unit.unit

        row['button_group'] = \
            f"""
            <div class="btn-group" style="display:flex; flex-wrap:nowrap;">
                <a class="btn btn-default btn-sm"  data-id={obj.id} href={reverse('adminlte_meter_indicator_update', kwargs={'pk': obj.id})} title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a> 
                <button class="btn btn-default btn-sm delete-button" data-href={reverse('adminlte_meter_indicator_delete', kwargs={'pk': obj.id})} title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """


class AdminMeterIndicatorDeleteView(MeterIndicatorPermissionRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        MeterIndicator.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})


class AdminListMeterIndicatorsView(
    MeterIndicatorPermissionRequiredMixin,
    TemplateView
):
    template_name = 'list_meter_indicators.html'


class AdminMeterIndicatorsDatatableView(AjaxDatatableView):
    model = MeterIndicator
    title = 'Показники лічильників'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    initial_order = [[0, 'asc']]

    column_defs = [
        {
            'name': 'pk',
            'visible': False,
            'orderable': True,
        },
        {
            'name': 'house__id',
            'title': 'Будинок',
            'className': 'house-filter',
            'choices': [(house.id, house.name) for house in House.objects.all()],
            'orderable': False,
        },
        {
            'name': 'section__id',
            'title': 'Секція',
            'className': 'section-filter',
            'choices': [],
            'orderable': False,
        },
        {
            'name': 'flat__no',
            'title': 'Номер квартири',
            'className': 'flat-filter',
            'choices': [],
        },
        {
            'name': 'service__id',
            'title': 'Послуга',
            'visible': True,
            'choices': [(service.id, service.name) for service in Service.objects.all()],
            'orderable': False
        },
        {
            'name': 'value',
            'title': 'Показник',
            'visible': True,
            'placeholder': True,
            'searchable': False,
            'orderable': False,
        },
        {
            'name': 'service__unit__unit',
            'title': 'Одиниця',
            'visible': True,
            'placeholder': True,
            'searchable': False,
            'orderable': False,
        },
        {
            'name': 'button_group',
            'title': '',
            'placeholder': True, 'visible': True,
            'searchable': False,
            'orderable': False,
        },
    ]

    def customize_row(self, row, obj):
        row['house__id'] = obj.house.name

        row['section__id'] = obj.section.name

        row['flat__no'] = obj.flat.no

        row['service__id'] = obj.service.name

        row['service__unit__unit'] = obj.service.unit.unit

        row['button_group'] = \
            f"""
            <div class="btn-group" style="display:flex; flex-wrap:nowrap;">
                <a href='{reverse_lazy('adminlte_meter_indicator_create')}?flat_id={obj.flat.id}&service_id={obj.service.id}' class="btn btn-default btn-sm" title="Додати нові показники">
                    <i class="fa fa-plus-circle"></i>
                </a> 
                <a href='{reverse_lazy('adminlte_meter_indicators_for_flat')}?flat_id={obj.flat.id}&service_id={obj.service.id}' class="btn btn-default btn-sm meter-indicator-for-flat-history" title="Переглянути історію показників">
                    <i class="fa fa-eye"></i>
                </a>
            </div>
            """
