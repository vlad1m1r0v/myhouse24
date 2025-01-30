from django.contrib.auth.models import Group
from django.db.models import Subquery, OuterRef
from django.views.generic import DetailView

from src.authentication.models import CustomUser
from .mixin import UserPermissionRequiredMixin


class AdminUserDetailView(UserPermissionRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'system_settings/adminlte/users/detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        role_subquery = Subquery(Group.objects.filter(user=OuterRef('pk')).order_by('id')[:1].values('name'))
        return super().get_queryset().annotate(role=role_subquery)