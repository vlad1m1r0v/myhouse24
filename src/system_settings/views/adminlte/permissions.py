from itertools import groupby

from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.authentication.models import CustomUser
from src.core.utils import CustomPermissionRequiredMixin
from src.system_settings.forms import AdminGroupPermissionFormSet


class RolePermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.payment_information'
    permission_denied_message = 'У Вас немає доступу до платіжних реквізитів'


class AdminGroupPermissionsView(RolePermissionRequiredMixin, TemplateView):
    template_name = 'system_settings/adminlte/permissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    gp.id,
                    g.id as group_id,
                    g.name as group_name,
                    p.id as permission_id
                FROM
                    auth_group g
                CROSS JOIN
                    auth_permission p
                LEFT JOIN
                    auth_group_permissions gp
                ON
                    gp.group_id = g.id
                AND
                    gp.permission_id = p.id
                WHERE
                    p.codename IN (
                        'statistics', 'cash_box', 'receipts', 'personal_accounts',
                        'flats', 'flat_owners', 'houses', 'messages', 'service_call_requests',
                        'meter_indicators', 'website_management', 'services', 'tariffs',
                        'roles', 'users', 'payment_information', 'payment_items'
                    )
                ORDER BY g.id, p.id
            """)

            rows = cursor.fetchall()

            formset = AdminGroupPermissionFormSet(
                initial=[
                    {'id': row[0],
                     'group_id': row[1],
                     'group_name': row[2],
                     'permission_id': row[3]}
                    for row in rows
                ]
            )

        grouped_formset = {group_name: list(forms) for group_name, forms in
                           groupby(formset, key=lambda form: form.initial.get('group_name'))}

        context['grouped_formset'] = grouped_formset
        context['management_form'] = formset.management_form

        return context

    def post(self, request, *args, **kwargs):
        formset = AdminGroupPermissionFormSet(request.POST)

        if formset.is_valid():
            for form in formset.forms:
                form.save()
            messages.success(self.request, "Дозволи для ролей успішно оновлені")
        else:
            print(formset.errors)
            messages.error(self.request, "Виникли деякі помилки при оновленні дозволів для ролей")
        return redirect('adminlte:system-settings:permissions:index')
