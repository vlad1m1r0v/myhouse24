from django.views.generic import TemplateView

from .mixin import FlatOwnerPermissionRequiredMixin
from ...forms import AdminFlatOwnersFiltersForm


class AdminFlatOwnersListView(FlatOwnerPermissionRequiredMixin,
                             TemplateView):
    template_name = 'flat_owners/adminlte/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filters'] = AdminFlatOwnersFiltersForm()

        return context
