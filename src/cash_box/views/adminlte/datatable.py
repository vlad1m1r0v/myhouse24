from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import Q, Sum
from django.template.loader import render_to_string

from src.cash_box.models import Transaction, TypeChoices


class AdminCashBoxDatatableView(AjaxDatatableView):
    model = Transaction

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'id'},
        {'name': 'no'},
        {'name': 'date'},
        {'name': 'is_complete'},
        {'name': 'payment_item'},
        {'name': 'owner'},
        {'name': 'personal_account'},
        {'name': 'type'},
        {'name': 'amount'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        qs = (self.model.objects
              .select_related('payment_item', 'owner', 'personal_account')
              .prefetch_related('personal_account__house__users'))

        if not request.user.is_superuser:
            qs = qs.filter(personal_account__house__users__in=[request.user.pk])

        return qs

    def footer_message(self, qs, params):
        totals = qs.filter(is_complete=True).aggregate(
            total_income=Sum('amount', filter=Q(type=TypeChoices.INCOME)),
            total_expense=Sum('amount', filter=Q(type=TypeChoices.EXPENSE))
        )

        income = totals.get('total_income') or 0.0
        expense = totals.get('total_expense') or 0.0

        return render_to_string(
            template_name='cash_box/adminlte/_partials/footer_message.html',
            context={'income': income, 'expense': expense}
        )

    def filter_queryset(self, params, qs):
        no = self.request.GET.get('no')
        daterange = self.request.GET.get('date')
        is_complete = self.request.GET.get('is_complete')
        payment_item = self.request.GET.get('payment_item')
        owner = self.request.GET.get('owner')
        personal_account = self.request.GET.get('personal_account')
        transaction_type = self.request.GET.get('type')

        filters = Q()

        if no:
            filters &= Q(no__icontains=no)

        if daterange:
            start = datetime.strptime(daterange.split(' - ')[0], '%d.%m.%Y')
            filters &= Q(date__gte=start)

            end = datetime.strptime(daterange.split(' - ')[1], '%d.%m.%Y')
            filters &= Q(date__lte=end)

        if is_complete:
            filters &= Q(is_complete=True if is_complete == 'True' else False)

        if payment_item:
            filters &= Q(payment_item__pk=payment_item)

        if owner:
            filters &= Q(owner__pk=owner)

        if personal_account:
            filters &= Q(personal_account__no__icontains=personal_account)

        if transaction_type:
            filters &= Q(type=transaction_type)

        return qs.filter(filters)

    def customize_row(self, row, obj):
        row['id'] = obj.id

        row['no'] = obj.no

        obj_date = datetime.strptime(str(obj.date), "%Y-%m-%d")
        row['date'] = obj_date.strftime("%d.%m.%Y")

        row['is_complete'] = 'Проведена' if obj.is_complete else 'Не проведена'

        row['payment_item'] = obj.payment_item.name

        row['owner'] = str(obj.owner) if obj.owner else '(Не вказано)'

        row['personal_account'] = str(obj.personal_account.no) if obj.personal_account else '(Не вказано)'

        row['type'] = render_to_string(
            template_name='cash_box/adminlte/_partials/type.html',
            context={'object': obj}
        )

        row['amount'] = render_to_string(
            template_name='cash_box/adminlte/_partials/amount.html',
            context={'object': obj}
        )

        row['actions'] = render_to_string(
            template_name='cash_box/adminlte/_partials/actions.html',
            context={'object': obj}
        )
