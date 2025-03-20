from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.loader import render_to_string

from src.personal_accounts.models import PersonalAccount


class AdminPersonalAccountsDatatableView(AjaxDatatableView):
    model = PersonalAccount

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'pk'},
        {'name': 'no'},
        {'name': 'status'},
        {'name': 'flat'},
        {'name': 'house'},
        {'name': 'section'},
        {'name': 'owner'},
        {'name': 'balance'},
        {'name': 'actions'},
    ]

    def get_initial_queryset(self, request=None):
        qs = (self.model.objects
            .with_balance()
            .with_debt()
            .select_related("house", "section", "flat", 'flat__owner'))

        if not self.request.user.is_superuser:
            qs = qs.filter(house__users__user=self.request.user)

        return qs

    def filter_queryset(self, params, qs):
        no = self.request.GET.get("no")
        status = self.request.GET.get("status")
        flat = self.request.GET.get('flat')
        house = self.request.GET.get('house')
        section = self.request.GET.get('section')
        owner = self.request.GET.get('owner')
        has_debt = self.request.GET.get('has_debt')

        filters = Q()

        if no:
            filters &= Q(no__icontains=no)

        if status:
            filters &= Q(status=status)

        if flat:
            filters &= Q(flat__no__icontains=flat)

        if house:
            filters &= Q(house__pk=house)

        if section:
            filters &= Q(section__pk=section)

        if owner:
            filters &= Q(flat__owner__pk=owner)

        if has_debt:
            filters &= Q(has_debt=True if has_debt == 'true' else False)

        return qs.filter(filters)

    def sort_queryset(self, params, qs):
        qs = qs.order_by('-id')
        return qs

    def customize_row(self, row, obj):
        row['pk'] = int(obj.pk)

        row['no'] = obj.no

        row['status'] = render_to_string(
            template_name='personal_accounts/adminlte/_partials/status.html',
            context={'object': obj}
        )

        row['flat'] = obj.flat.no if obj.flat else '(Не вказано)'

        row['house'] = obj.house.name if obj.house else '(Не вказано)'

        row['section'] = obj.section.name if obj.section else '(Не вказано)'

        row['owner'] = f"{obj.flat.owner.last_name} {obj.flat.owner.first_name} {obj.flat.owner.middle_name}" if obj.flat else '(Не вказано)'

        row['balance'] = render_to_string(
            template_name='personal_accounts/adminlte/_partials/balance.html',
            context={'object': obj}
        )

        row['actions'] = render_to_string(
            template_name='personal_accounts/adminlte/_partials/actions.html',
            context={'object': obj}
        )
