from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Value, F, CharField, Q, ExpressionWrapper, DateTimeField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from datetime import datetime

from src.authentication.models import CustomUser
from src.core.utils import is_ajax
from src.flats.models import Flat
from src.master_call_requests.forms import AdminMasterCallRequestForm
from src.master_call_requests.models import MasterCallRequest, StatusChoices


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
    success_url = reverse_lazy('adminlte_master_call_requests_list')
    form_class = AdminMasterCallRequestForm
    template_name = 'create_master_call_request.html'


class AdminMasterCallRequestUpdateView(
    SuccessMessageMixin,
    MasterCallRequestPermissionRequiredMixin,
    UpdateView):
    success_message = 'Заявку виклику майстра успішно оновлено'
    success_url = reverse_lazy('adminlte_master_call_requests_list')
    model = MasterCallRequest
    form_class = AdminMasterCallRequestForm
    template_name = 'update_master_call_request.html'


class AdminMasterCallRequestDetailView(
    MasterCallRequestPermissionRequiredMixin,
    DetailView
):
    model = MasterCallRequest
    template_name = 'detail_master_call_request.html'


class AdminMasterCallRequestListView(
    MasterCallRequestPermissionRequiredMixin,
    TemplateView
):
    template_name = 'list_master_call_requests.html'


class AdminMasterCallRequestDatatableView(AjaxDatatableView):
    model = MasterCallRequest
    title = 'Заявки виклику майстра'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    initial_order = [[0, 'asc']]

    column_defs = [
        {
            'name': 'pk',
            'title': 'Номер заявки',
        },
        {
            'name': 'datetime',
            'title': 'Зручний час',
            'placeholder': True,
            'searchable': True,
            'orderable': True,
            'className': 'daterange-filter',
        },
        {
            'name': 'master_type',
            'title': 'Тип майстера',
            'className': 'master-type-select',
            'placeholder': True,
            'choices': [(group.id, group.name) for group in Group.objects.filter(name__in=['Сантехнік', 'Електрик'])]
        },
        {
            'name': 'description',
            'title': 'Опис',
            'searchable': True,
            'orderable': False,
        },
        {
            'name': 'flat__no',
            'title': 'Квартира',
            'placeholder': True,
            'searchable': True,
            'orderable': False,
        },
        {
            'name': 'flat_owner__pk',
            'title': 'Власник',
            'searchable': True,
            'orderable': False,
            'choices': [(user.id, f'{user.last_name} {user.first_name} {user.middle_name}') for user in
                        CustomUser.objects.filter(is_staff=False)]
        },
        {
            'name': 'flat_owner__phone_number',
            'title': 'Телефон',
            'searchable': True,
            'orderable': False,
        },
        {
            'name': 'master__pk',
            'title': 'Майстер',
            'className': 'master-select',
            'searchable': True,
            'orderable': False,
            'choices': [(master.id, f'{master.first_name} {master.last_name} - {master.groups.first().name}') for master
                        in CustomUser.objects.filter(groups__name__in=['Сантехнік', 'Електрик'])]
        },
        {
            'name': 'status',
            'title': 'Статус',
            'visible': True,
            'choices': StatusChoices.choices,
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
        return self.model.objects.annotate(
            datetime=ExpressionWrapper(
                F('date') + F('time'),
                output_field=DateTimeField()
            )
        )

    def filter_queryset(self, params, qs):
        for column_link in params['column_links']:
            if column_link.searchable and column_link.search_value:
                if column_link.name == 'datetime':
                    date_range = column_link.search_value

                    date_start = datetime.strptime(date_range.split(' - ')[0], '%d.%m.%Y')
                    date_end = datetime.strptime(date_range.split(' - ')[1], '%d.%m.%Y')

                    qs = qs.filter(Q(datetime__gte=date_start), Q(datetime__lte=date_end))
                elif column_link.name == 'master_type':
                    qs = qs.filter(master_type__id=column_link.search_value)
                else:
                    qs = self.filter_queryset_by_column(column_link.name, column_link.search_value, qs)
        return qs

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'datetime':
                if order.ascending:
                    return qs.order_by('datetime')
                return qs.order_by('-datetime')

            break

        return super().sort_queryset(params, qs)

    def customize_row(self, row, obj):
        row['datetime'] = obj.datetime.strftime("%d.%m.%Y - %H:%M")

        if not obj.master_type:
            row['master_type'] = 'Будь-який спеціаліст'

        row['flat__no'] = f"кв.{obj.flat.no}, {obj.flat.house.name}"

        row['flat_owner__pk'] = f'{obj.flat_owner.last_name} {obj.flat_owner.first_name} {obj.flat_owner.middle_name}'

        row['flat_owner__phone_number'] = obj.flat_owner.phone_number

        if not obj.master:
            row['master__pk'] = 'Не задано'

        row['master__pk'] = f'{obj.master.first_name} {obj.master.last_name} - {obj.master.groups.first().name}'

        row['button_group'] = \
            f"""
            <div class="btn-group" style="display:flex; flex-wrap:nowrap;">
                <a class="btn btn-default btn-sm" href={reverse('adminlte_master_call_request_update', kwargs={'pk': obj.id})} title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a> 
                <button class="btn btn-default btn-sm delete-button" data-href={reverse('adminlte_master_call_request_delete', kwargs={'pk': obj.id})} title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """

        if obj.status == 'new':
            row['status'] = f"<small class='label label-primary'>{obj.get_status_display()}</small>"
        if obj.status == 'in_progress':
            row['status'] = f"<small class='label label-warning'>{obj.get_status_display()}</small>"
        if obj.status == 'done':
            row['status'] = f"<small class='label label-success'>{obj.get_status_display()}</small>"


class AdminMasterCallRequestDeleteView(MasterCallRequestPermissionRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        MasterCallRequest.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
