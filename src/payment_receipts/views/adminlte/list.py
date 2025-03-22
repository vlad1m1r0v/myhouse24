from django.views.generic import TemplateView

from src.dashboard.views.adminlte.mixin import AdminBalanceMixin
from src.flats.models import Flat
from .mixin import ReceiptsPermissionRequiredMixin
from ...forms import AdminReceiptFiltersForm


class AdminReceiptsListView(
    AdminBalanceMixin,
    ReceiptsPermissionRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/adminlte/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        initial = {}

        flat_id = self.request.GET.get('flat_id')

        if flat_id:
            flat_no = Flat.objects.get(id=flat_id).no
            initial['flat'] = flat_no

        context['filters'] = AdminReceiptFiltersForm(initial=initial)

        return context
