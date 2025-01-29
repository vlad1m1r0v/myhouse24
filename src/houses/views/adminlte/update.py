from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.authentication.models import CustomUser
from src.houses.forms import (
    AdminHouseForm,
    AdminHouseSectionFormSet,
    AdminHouseFloorFormSet,
    AdminHouseUserFormSet
)
from src.houses.models import House, HouseUser
from .mixin import (
    HousePermissionRequiredMixin,
    HouseUserRequiredMixin
)


class AdminHouseUpdateView(
    HousePermissionRequiredMixin,
    HouseUserRequiredMixin,
    TemplateView):
    template_name = 'houses/adminlte/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        house = House.objects.prefetch_related(
            Prefetch('users', queryset=HouseUser.objects.select_related('user'))
        ).get(pk=self.kwargs['pk'])

        context['house'] = AdminHouseForm(instance=house)
        context['sections'] = AdminHouseSectionFormSet(instance=house)
        context['floors'] = AdminHouseFloorFormSet(instance=house)
        context['users'] = AdminHouseUserFormSet(instance=house, queryset=house.users.all())

        return context

    def post(self, *args, **kwargs):
        instance = House.objects.get(pk=kwargs.get('pk'))

        house = AdminHouseForm(self.request.POST, self.request.FILES, instance=instance)
        sections = AdminHouseSectionFormSet(self.request.POST, instance=instance)
        floors = AdminHouseFloorFormSet(self.request.POST, instance=instance)
        users = AdminHouseUserFormSet(self.request.POST, instance=instance)

        if all([house.is_valid(), sections.is_valid(), floors.is_valid(), users.is_valid()]):
            house.save()
            sections.save()
            floors.save()
            users.save()
            messages.success(self.request, 'Будинок успішно оновлено')
        else:
            messages.error(self.request, 'Виникли певні посилки при оновленні будинку')
        return redirect(reverse('adminlte:houses:list'))
