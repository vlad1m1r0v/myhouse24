from django.views.generic import TemplateView

from src.core.utils.permissions import OwnerRequiredMixin
from src.payment_receipts.forms import AccountReceiptFiltersForm


class AccountReceiptsListView(
    OwnerRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/account/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filters'] = AccountReceiptFiltersForm()

        return context