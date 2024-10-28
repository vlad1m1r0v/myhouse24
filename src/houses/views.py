from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, View

from src.core.utils import is_ajax
from src.houses.forms import AdminHouseForm, AdminHouseSectionFormSet, AdminHouseFloorFormSet, AdminHouseUserFormSet
from src.houses.models import House


class HousePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.houses'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до домівок'})
            else:
                messages.error(request, 'У Вас немає доступу до домівок')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


class HouseUserMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')

        has_permission = user.is_superuser or House.objects.filter(pk=pk, users__user=user).exists()

        print({has_permission})

        if not has_permission:
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до будинку'})
            else:
                messages.error(request, 'У Вас немає доступу до будинку')
                return redirect(reverse('adminlte_houses_list'))
        return super().dispatch(request, *args, **kwargs)


class AdminHousesListView(HousePermissionRequiredMixin,
                          TemplateView):
    template_name = 'houses/list_houses.html'


class AdminHouseCreateView(HousePermissionRequiredMixin,
                           TemplateView):
    template_name = 'houses/create_house.html'

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
            messages.error(self.request, 'Виникли певні посилки при створенні домівки')
        return redirect(reverse('adminlte_houses_list'))


class AdminHouseDetailView(
    HousePermissionRequiredMixin,
    HouseUserMixin,
    DetailView):
    template_name = 'houses/detail_house.html'
    model = House
    context_object_name = 'house'


class AdminHouseUpdateView(
    HousePermissionRequiredMixin,
    HouseUserMixin,
    TemplateView):
    template_name = 'houses/update_house.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        house = House.objects.get(pk=self.kwargs['pk'])

        context['house'] = AdminHouseForm(instance=house)
        context['sections'] = AdminHouseSectionFormSet(instance=house)
        context['floors'] = AdminHouseFloorFormSet(instance=house)
        context['users'] = AdminHouseUserFormSet(instance=house)

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
            messages.success(self.request, 'Домівку успішно оновлено')
        else:
            messages.error(self.request, 'Виникли певні посилки при оновленні домівки')
        return redirect(reverse('adminlte_houses_list'))


class AdminHousesDatatableView(AjaxDatatableView):
    model = House
    title = 'Домівки'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': '#', 'visible': True, },
        {'name': 'name', 'title': 'Назва', 'visible': True, },
        {'name': 'address', 'title': 'Адреса', 'visible': True},
        {'name': 'button_group',
         'title': '',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False,
         },
    ]

    def customize_row(self, row, obj):
        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                 <a href={reverse('adminlte_house_update', kwargs={'pk': obj.id})} class="btn btn-default btn-sm" title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a>
                <button data-href={reverse('adminlte_house_delete', kwargs={'pk': obj.id})} class="btn btn-default btn-sm delete-button" title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """

    def get_initial_queryset(self, request=None):
        user = request.user
        if user.is_superuser:
            return super().get_initial_queryset(request)
        return super().get_initial_queryset(request).filter(users__user=user)


class AdminHousesDeleteView(
    HousePermissionRequiredMixin,
    HouseUserMixin,
    View):
    permission_required = ('authentication.houses',)

    def delete(self, request, *args, **kwargs):
        House.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
