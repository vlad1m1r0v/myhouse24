from django.db.models import Prefetch
from django.views.generic import DetailView

from src.authentication.models import CustomUser
from src.flats.models import Flat

from .mixin import (
    HouseUserRequiredMixin,
    FlatOwnerPermissionRequiredMixin
)


class AdminFlatOwnerDetailView(
    HouseUserRequiredMixin,
    FlatOwnerPermissionRequiredMixin,
    DetailView):
    model = CustomUser
    template_name = 'flat_owners/adminlte/detail.html'
    context_object_name = 'profile'

    def get_queryset(self, queryset=None):
        return (super().get_queryset()
        .prefetch_related(Prefetch(
            'flats', queryset=Flat.objects.select_related('house', 'section', 'personal_account')
        )))
