from django.views.generic import DetailView

from .mixin import (
    HouseUserRequiredMixin,
    FlatPermissionRequiredMixin
)
from ...models import Flat


class AdminFlatDetailView(
    FlatPermissionRequiredMixin,
    HouseUserRequiredMixin,
    DetailView
):
    template_name = 'flats/adminlte/detail.html'
    model = Flat
    context_object_name = 'flat'

    def get_queryset(self, **kwargs):
        return super().get_queryset().select_related('house', 'section', 'floor', 'tariff', 'owner')

