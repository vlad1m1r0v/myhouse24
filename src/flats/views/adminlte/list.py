from django.views.generic import TemplateView
from .mixin import FlatPermissionRequiredMixin
from ...forms import AdminFlatsFiltersForm


class AdminFlatsListView(
    FlatPermissionRequiredMixin,
    TemplateView
):
    template_name = 'flats/adminlte/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filters'] = AdminFlatsFiltersForm()

        return context