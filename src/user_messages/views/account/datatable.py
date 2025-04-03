from ajax_datatable import AjaxDatatableView
from django.contrib.auth.models import Group
from django.db.models import Q, Subquery, OuterRef
from django.template.loader import render_to_string

from src.flats.models import Flat
from src.payment_receipts.models import Receipt
from src.user_messages.models import Message, ReadMessage


class AccountMessagesDatatableView(AjaxDatatableView):
    model = Message

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'id'},
        {'name': 'creator'},
        {'name': 'text'},
        {'name': 'date'},
    ]

    def get_initial_queryset(self, request=None):
        user = request.user

        has_debt = (Receipt.objects
                    .filter(status__in=['unpaid', 'partially_paid'], flat__owner=user)
                    .select_related('flat', 'flat__owner')
                    .exists())

        read_messages = ReadMessage.objects.filter(user=user.id).values_list('message_id', flat=True)

        flats = Flat.objects.filter(owner=user.id)

        houses_ids = [flat.house.id for flat in flats]
        sections_ids = [flat.section.id for flat in flats]
        floors_ids = [flat.floor.id for flat in flats]
        flats_ids = [flat.id for flat in flats]

        filters = Q()

        filters |= Q(
            house__isnull=True,
            section__isnull=True,
            floor__isnull=True,
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__isnull=True,
            floor__isnull=True,
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__in=[*sections_ids],
            floor__isnull=True,
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__in=[*sections_ids],
            floor__in=[*floors_ids],
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__in=[*sections_ids],
            floor__in=[*floors_ids],
            flat__in=[*flats_ids],
            flat_owner__isnull=True
        )

        filters |= Q(
            house__isnull=True,
            section__isnull=True,
            floor__isnull=True,
            flat__isnull=True,
            flat_owner=user
        )

        if not has_debt:
            filters &= Q(to_debtors=False)

        filters &= ~Q(id__in=read_messages)

        role_subquery = Subquery(Group.objects
                                 .filter(user=OuterRef('creator__pk'))
                                 .order_by('id')[:1]
                                 .values('name'))

        return (self.model.objects
                .select_related('creator')
                .filter(filters)
                .annotate(role=role_subquery))

    def filter_queryset(self, params, qs):
        search = self.request.GET.get('search')
        filters = Q()

        if search:
            filters &= Q(description__icontains=search)
            filters |= Q(topic__icontains=search)

        qs = qs.filter(filters)
        return qs

    def sort_queryset(self, params, qs):
        return qs.order_by('-id')

    def customize_row(self, row, obj):
        row['id'] = obj.id

        row['creator'] = render_to_string(
            template_name='user_messages/account/_partials/creator.html',
            context={'object': obj}
        )

        row['text'] = render_to_string(
            template_name='user_messages/shared/_partials/text.html',
            context={'object': obj}
        )

        row['date'] = render_to_string(
            template_name='user_messages/shared/_partials/date.html',
            context={'object': obj}
        )
