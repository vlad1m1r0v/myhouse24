from django.views.generic import TemplateView

from .mixin import MasterCallRequestPermissionRequiredMixin
from ...forms import AdminMasterCallRequestFiltersForm


class AdminMasterCallRequestsListView(
    MasterCallRequestPermissionRequiredMixin,
    TemplateView
):
    template_name = 'master_call_requests/adminlte/list.html'

    def get_context_data(self, **kwargs):
        context = super(AdminMasterCallRequestsListView, self).get_context_data(**kwargs)

        context['filters'] = AdminMasterCallRequestFiltersForm()

        return context