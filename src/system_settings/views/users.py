from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Value, Subquery, OuterRef, Q
from django.db.models.functions import Concat, Coalesce
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DetailView

from src.authentication.models import CustomUser, STATUS_CHOICES
from src.core.utils import is_ajax
from src.system_settings.forms import AdminUserForm


class UserPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.users'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до статей користувачів'})
            else:
                messages.error(request, 'У Вас немає доступу до користувачів')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


class AdminUsersView(UserPermissionRequiredMixin,
                     TemplateView):
    template_name = 'system_settings/users/list_users.html'


class AdminUsersDatatableView(AjaxDatatableView):
    model = CustomUser
    title = 'Користувачі'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': '#', 'visible': True, },
        {'name': 'full_name', 'title': 'Користувач', 'visible': True, },
        {'name': 'role',
         'title': 'Роль',
         'visible': True,
         'choices': [(group.name, group.name) for group in Group.objects.all()],
         },
        {'name': 'phone_number', 'title': 'Номер телефону', 'visible': True},
        {'name': 'email', 'title': 'Електронна пошта', 'visible': True},
        {'name': 'status',
         'title': 'Статус',
         'visible': True,
         'choices': STATUS_CHOICES,
         },
        {'name': 'button_group',
         'title': '',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False,
         },
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).annotate(
            role=Coalesce(
                Subquery(
                    Group.objects.filter(user=OuterRef('pk')).values('name')[:1]
                ),
                Value(None)
            )
        )

    def customize_row(self, row, obj):
        if obj.status == 'new':
            row['status'] = f"<small class='label label-warning'>{obj.get_status_display()}</small>"
        elif obj.status == 'active':
            row['status'] = f"<small class='label label-success'>{obj.get_status_display()}</small>"
        else:
            row['status'] = f"<small class='label label-danger'>{obj.get_status_display()}</small>"

        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                <a class="btn btn-default btn-sm" title='Надіслати запрошення'>
                    <i class="fa fa-repeat"></i>
                </a>
                 <a href={reverse('adminlte_user_update', kwargs={'pk': obj.id})} class="btn btn-default btn-sm" title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a>
                <button {'disabled' if self.request.user.id == obj.id or obj.is_superuser else ''} {'data-href=' + reverse('adminlte_user_delete', kwargs={'pk': obj.id}) if self.request.user.id != obj.id else ''} class="btn btn-default btn-sm delete-button"  title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """


class AdminUserDetailView(UserPermissionRequiredMixin,
                          DetailView):
    model = CustomUser
    template_name = 'system_settings/users/detail_user.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['role'] = user.groups.first() if user.groups.exists() else None
        return context


class AdminUserUpdateView(SuccessMessageMixin,
                          UserPermissionRequiredMixin,
                          UpdateView):
    model = CustomUser
    form_class = AdminUserForm
    template_name = 'system_settings/users/update_user.html'
    success_url = reverse_lazy('adminlte_users_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Дані користувача успішно оновлено")

        if form.instance == self.request.user:
            update_session_auth_hash(self.request, form.instance)

        return response

    def form_invalid(self, form):
        messages.error(self.request, "Помилка при оновленні данних користувача")
        return super().form_invalid(form)


class AdminUserCreateView(SuccessMessageMixin,
                          UserPermissionRequiredMixin,
                          CreateView):
    model = CustomUser
    template_name = 'system_settings/users/create_user.html'
    form_class = AdminUserForm
    success_url = reverse_lazy('adminlte_users_list')
    success_message = 'Новий користувач успішно створений'


class AdminUserDeleteView(UserPermissionRequiredMixin,
                          View):
    def delete(self, request, *args, **kwargs):
        CustomUser.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
