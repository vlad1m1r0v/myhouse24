from django.views.generic import TemplateView

from .mixin import HousePermissionRequiredMixin


class AdminHousesListView(HousePermissionRequiredMixin,
                          TemplateView):
    template_name = 'houses/adminlte/list.html'