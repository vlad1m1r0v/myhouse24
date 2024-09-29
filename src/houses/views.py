from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.houses.forms import AdminHouseForm, AdminHouseSectionFormSet, AdminHouseFloorFormSet, AdminHouseUserFormSet


class AdminHouseCreateView(TemplateView):
    template_name = 'houses/create_house.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['house'] = AdminHouseForm()
        context['sections'] = AdminHouseSectionFormSet()
        context['floors'] = AdminHouseFloorFormSet()
        context['users'] = AdminHouseUserFormSet()

        return context

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до домівок')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))
