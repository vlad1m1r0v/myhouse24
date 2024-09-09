from ajax_datatable.views import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, View

from src.system_settings.forms import AdminTariffForm, AdminTariffServiceFormSet
from src.system_settings.models import Tariff


class AdminTariffsView(PermissionRequiredMixin, TemplateView):
    permission_required = ('authentication.tariffs',)
    template_name = 'system_settings/tariffs/list_tariffs.html'

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до тарифів')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))


class AdminTariffsDatatableView(AjaxDatatableView):
    model = Tariff
    title = 'Тарифи'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'name', 'title': 'Назва', 'visible': True, 'searchable': False},
        {'name': 'description', 'title': 'Опис', 'visible': True, 'searchable': False, },
        {'name': 'updated_at', 'title': 'Дата редагування', 'visible': True, 'searchable': False, },
        {'name': 'button_group', 'title': '', 'placeholder': True, 'visible': True, 'searchable': False,
         'orderable': False, },
    ]

    def customize_row(self, row, obj):
        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                <a class="btn btn-default btn-sm" title='Копіювати'>
                    <i class="fa fa-clone"></i>
                </a>
                 <a href={reverse('adminlte_tariff_update', kwargs={'pk': obj.id})} class="btn btn-default btn-sm" title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a>
                <button data-href={reverse('adminlte_tariff_delete', kwargs={'pk': obj.id})} class="btn btn-default btn-sm delete-button">
                    <i class="fa fa-trash" title="Видалити"></i>
                </button>
            </div>
            """

        row['updated_at'] = str(obj.updated_at.strftime("%d.%m.%Y-%-H:%M"))


class AdminTariffDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'system_settings/tariffs/detail_tariff.html'
    permission_required = ('authentication.tariffs',)
    model = Tariff
    context_object_name = 'tariff'

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до тарифів')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))


class AdminTariffUpdateView(PermissionRequiredMixin, TemplateView):
    permission_required = ('authentication.tariffs',)
    template_name = 'system_settings/tariffs/update_tariff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tariff = Tariff.objects.get(pk=self.kwargs['pk'])

        context['tariff'] = AdminTariffForm(instance=tariff)
        context['services'] = AdminTariffServiceFormSet(
            instance=tariff,
            prefix='service'
        )

        return context

    def post(self, *args, **kwargs):
        instance = Tariff.objects.get(pk=self.kwargs['pk'])
        tariff = AdminTariffForm(self.request.POST, instance=instance)
        services = AdminTariffServiceFormSet(self.request.POST, instance=instance, prefix='service')

        if tariff.is_valid() and services.is_valid():
            tariff.save()
            services.save()
            messages.success(self.request, 'Інформацію про тариф успішно оновлено')
            return redirect(reverse('adminlte_tariffs_list'))
        else:
            for form_errors in services.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)

            return self.render_to_response(self.get_context_data(tariff=tariff, services=services))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до тарифів')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))


class AdminTariffCreateView(PermissionRequiredMixin, TemplateView):
    permission_required = ('authentication.tariffs',)
    template_name = 'system_settings/tariffs/create_tariff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tariff_id = self.request.GET.get('tariff_id', None)

        if tariff_id:
            tariff = Tariff.objects.get(pk=tariff_id)

            form = AdminTariffForm(
                initial={
                    'name': tariff.name,
                    'description': tariff.description
                },
                instance=tariff)
            formset = AdminTariffServiceFormSet(
                instance=tariff,
                prefix='service',
            )
        else:
            form = AdminTariffForm()
            formset = AdminTariffServiceFormSet(prefix='service')

        context['tariff'] = form
        context['services'] = formset

        return context

    def post(self, *args, **kwargs):
        form = AdminTariffForm(self.request.POST)
        formset = AdminTariffServiceFormSet(self.request.POST, prefix='service')

        if form.is_valid() and formset.is_valid():
            tariff = form.save()
            formset.instance = tariff
            formset.save()

            messages.success(self.request, 'Тариф успішно створено')
            return redirect(reverse('adminlte_tariffs_list'))
        else:
            for form_errors in formset.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)

            return self.render_to_response(self.get_context_data(tariff=form, services=formset))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до тарифів')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))


class AdminTariffDeleteView(PermissionRequiredMixin, View):
    permission_required = ('authentication.tariffs',)

    def delete(self, request, *args, **kwargs):
        Tariff.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до тарифів')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))
