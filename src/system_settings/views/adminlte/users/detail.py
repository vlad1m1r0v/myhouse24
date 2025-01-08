from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from src.authentication.models import CustomUser
from .mixin import UserPermissionRequiredMixin


class AdminUserDetailView(UserPermissionRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'system_settings/adminlte/users/detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        return CustomUser.objects.prefetch_related('groups')

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['role'] = user.groups.first() if user.groups.exists() else None
        return context