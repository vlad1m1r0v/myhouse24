from itertools import groupby

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import connection
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from src.system_settings.forms import AdminGroupPermissionFormSet



class AdminGroupPermissionsView(PermissionRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'system_settings/permissions.html'
    permission_required = ('authentication.roles',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    gp.id,
                    g.id as group_id,
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
                     'permission_id': row[2]}
                    for row in rows
                ]
            )

        grouped_formset = {group_id: list(forms) for group_id, forms in
                           groupby(formset, key=lambda form: form.initial.get('group_id'))}

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
            messages.error(self.request, "Виникли деякі помилки при оновленні дозволів для ролей")
        return redirect('adminlte_permissions')

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до управління дозволами')
        return redirect(reverse('authentication_adminlte_login'))
