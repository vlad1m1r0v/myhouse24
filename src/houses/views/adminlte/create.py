from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.houses.forms import (
    AdminHouseForm,
    AdminHouseSectionFormSet,
    AdminHouseFloorFormSet,
    AdminHouseUserFormSet
)
from .mixin import HousePermissionRequiredMixin


class AdminHouseCreateView(HousePermissionRequiredMixin,
                           TemplateView):
    template_name = 'houses/adminlte/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['house'] = AdminHouseForm()
        context['sections'] = AdminHouseSectionFormSet()
        context['floors'] = AdminHouseFloorFormSet()
        context['users'] = AdminHouseUserFormSet()

        return context

    def post(self, *args, **kwargs):
        house = AdminHouseForm(self.request.POST, self.request.FILES)
        sections = AdminHouseSectionFormSet(self.request.POST, self.request.FILES)
        floors = AdminHouseFloorFormSet(self.request.POST, self.request.FILES)
        users = AdminHouseUserFormSet(self.request.POST, self.request.FILES)

        if all([house.is_valid(), sections.is_valid(), floors.is_valid(), users.is_valid()]):
            instance = house.save()

            sections.instance = instance
            sections.save()

            floors.instance = instance
            floors.save()

            users.instance = instance
            users.save()

            messages.success(self.request, 'Будинок успішно створено')
        else:
            messages.error(self.request, 'Виникли певні посилки при створенні будинку')
        return redirect(reverse('adminlte:houses:list'))
