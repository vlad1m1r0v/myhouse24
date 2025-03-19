from django.db.models import Sum, Value, DecimalField, Case, When, F
from django.db.models.functions import Coalesce
from django.views.generic import DetailView

from src.cash_box.models import TypeChoices
from src.personal_accounts.models import PersonalAccount


class AdminPersonalAccountDetailView(DetailView):
    model = PersonalAccount
    context_object_name = 'personal_account'
    template_name = 'personal_accounts/adminlte/detail.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("house", "section", "flat", "flat__owner")
            .annotate(
                income=Coalesce(
                    Sum(
                        Case(
                            When(
                                account_transactions__type=TypeChoices.INCOME,
                                account_transactions__is_complete=True,
                                then=F("account_transactions__amount")
                            ),
                            default=Value(0.0),
                            output_field=DecimalField()
                        )
                    ),
                    Value(0.0),
                    output_field=DecimalField()
                ),
                expense=Coalesce(
                    Sum(
                        Case(
                            When(
                                account_transactions__type=TypeChoices.EXPENSE,
                                account_transactions__is_complete=True,
                                account_transactions__receipt__isnull=False,
                                then=F("account_transactions__amount")
                            ),
                            default=Value(0.0),
                            output_field=DecimalField()
                        )
                    ),
                    Value(0.0),
                    output_field=DecimalField()
                )
            )
            .annotate(balance=F("income") - F("expense"))
        )
