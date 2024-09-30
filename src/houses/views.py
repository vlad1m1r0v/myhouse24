from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from src.houses.forms import AdminHouseForm, AdminHouseSectionFormSet, AdminHouseFloorFormSet, AdminHouseUserFormSet
from src.houses.models import House


class AdminHouseCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'houses/create_house.html'
    permission_required = 'authentication.houses'

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

            messages.success(self.request, 'Домівку успішно створено')
        else:
            messages.success(self.request, 'Виникли певні посилки при створенні домівки')
            print(users.errors)
        return redirect(reverse('adminlte_houses_create'))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до домівок')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))


class AdminHouseDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'authentication.houses'
    template_name = 'houses/detail_house.html'
    model = House
    context_object_name = 'house'

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до домівок')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))
