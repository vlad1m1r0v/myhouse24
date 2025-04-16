from django.db.models import Sum, Min, Max
from django.views.generic import TemplateView

from src.cash_box.models import Transaction
from src.core.utils.permissions import OwnerRequiredMixin
from src.flats.models import Flat
from src.personal_accounts.models import PersonalAccount


class AccountDashboardView(OwnerRequiredMixin, TemplateView):
    template_name = 'dashboard/account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flat_id = self.request.GET.get('flat_id')
        flat = Flat.objects.select_related('house').get(id=flat_id)
        context['flat'] = flat

        balance = PersonalAccount.objects.with_balance().get(flat_id=flat_id)
        context['balance'] = balance

        expenses = Transaction.objects.filter(personal_account=balance.pk, type='expense', is_complete=True)

        dates = expenses.aggregate(start=Min('date'), end=Max('date'))

        start_date = dates['start']
        end_date = dates['end']

        if start_date and end_date:
            month_count = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

            total = expenses.aggregate(total=Sum('amount'))['total'] or 0
            avg_per_month = total / month_count
        else:
            avg_per_month = 0

        context['avg_per_month'] = avg_per_month

        return context
