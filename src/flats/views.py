from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View

from src.authentication.models import CustomUser
from src.core.utils import is_ajax
from src.flats.forms import AdminFlatForm
from src.houses.models import House, HouseSection, HouseFloor
from src.personal_accounts.models import PersonalAccount
from src.system_settings.models import Tariff


class FlatPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.flats'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до квартир'})
            else:
                messages.error(request, 'У Вас немає доступу до квартир')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
class AdminCreateFlatView(FlatPermissionRequiredMixin,
                          CreateView):
    template_name = 'flats/create_flat.html'
    form_class = AdminFlatForm
    # TODO: change to flats list page URL
    success_url = reverse_lazy('adminlte_flat_create')

    def form_valid(self, form):
        new_personal_account = form.cleaned_data.get('new_personal_account')

        flat = form.save()

        if new_personal_account:
            personal_account = PersonalAccount.objects.create(
                no=new_personal_account,
                house=form.cleaned_data.get('house'),
                section=form.cleaned_data.get('section'),
                flat=flat
            )

            flat.personal_account = personal_account
            flat.save()

            messages.success(self.request, 'Нову квартиру успішно створено')

        return HttpResponseRedirect(self.success_url)


class AdminFlatHousesView(FlatPermissionRequiredMixin,
                          View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        user = request.user
        if user.is_superuser:
            houses = House.objects.filter(name__icontains=term).values('id', 'name')
        else:
            houses = House.objects.filter(users__user=user)
        return JsonResponse(data=list(houses), safe=False)


class AdminFlatSectionsView(FlatPermissionRequiredMixin,
                            View):
    def get(self, request, *args, **kwargs):
        house_id = request.GET.get('house_id')
        term = request.GET.get('term', '')
        sections = HouseSection.objects.filter(house__id=house_id, name__icontains=term).values('id', 'name')
        return JsonResponse(data=list(sections), safe=False)


class AdminFlatFloorsView(FlatPermissionRequiredMixin,
                          View):
    def get(self, request, *args, **kwargs):
        house_id = request.GET.get('house_id')
        term = request.GET.get('term', '')
        floors = HouseFloor.objects.filter(house__id=house_id, name__icontains=term).values('id', 'name')
        return JsonResponse(data=list(floors), safe=False)


class AdminFlatOwnersView(FlatPermissionRequiredMixin,
                          View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        owners = CustomUser.objects.annotate(
            full_name=Concat('last_name',
                             Value(' '),
                             'first_name',
                             Value(' '),
                             'middle_name')).filter(
            is_staff=False, full_name__icontains=term
        ).exclude(status='disabled').values('full_name', 'id')
        return JsonResponse(data=list(owners), safe=False)


class AdminFlatTariffsView(FlatPermissionRequiredMixin,
                           View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        tariffs = Tariff.objects.filter(name__icontains=term).values('name', 'id')
        return JsonResponse(data=list(tariffs), safe=False)
