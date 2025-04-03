from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.loader import render_to_string

from src.user_messages.models import Message


class AdminMessagesDatatableView(AjaxDatatableView):
    model = Message

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    initial_order = [["id", "desc"], ]

    column_defs = [
        {'name': 'id'},
        {'name': 'receivers'},
        {'name': 'text'},
        {'name': 'date'},
    ]

    def get_initial_queryset(self, request=None):
        qs = self.model.objects.select_related('house', 'section', 'floor', 'flat')
        return qs

    def sort_queryset(self, params, qs):
        qs = qs.order_by('-id')
        return qs

    def filter_queryset(self, params, qs):
        search = self.request.GET.get('search')
        filters = Q()

        if search:
            filters &= Q(description__icontains=search)
            filters |= Q(topic__icontains=search)

        qs = qs.filter(filters)
        return qs

    def customize_row(self, row, obj):
        row['id'] = obj.id

        row['receivers'] = render_to_string(
            template_name='user_messages/adminlte/_partials/receivers.html',
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
