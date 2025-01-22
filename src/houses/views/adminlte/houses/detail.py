from django.contrib.auth.models import Group
from django.db.models import Prefetch
from django.views.generic import DetailView

from src.houses.models import House
from .mixin import HousePermissionRequiredMixin, HouseUserRequiredMixin


class AdminHouseDetailView(
    HousePermissionRequiredMixin,
    HouseUserRequiredMixin,
    DetailView):
    template_name = 'houses/adminlte/detail.html'
    model = House
    context_object_name = 'house'

    def get_queryset(self):
        """
        Оптимізуємо запити до бази даних за допомогою select_related і prefetch_related.
        """
        return (
            super().get_queryset()
            .prefetch_related(
                'users__user',
                Prefetch(
                    'users__user__groups',
                    queryset=Group.objects.order_by('id')[:1],
                    to_attr='first_group'
                ),
                'sections',
                'floors'
            )
        )
