from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from django.db.models import F, Value
from src.core.utils import is_ajax
from src.flats.models import Flat
from src.personal_accounts.forms import AdminPersonalAccountForm
from src.personal_accounts.models import PersonalAccount


class PersonalAccountPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.personal_accounts'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False,
                                          'message': 'У Вас немає доступу до особових рахунків'})
            else:
                messages.error(request, 'У Вас немає доступу до особових рахунків')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


# Create your views here.

class AdminPersonaAccountCreateView(SuccessMessageMixin,
                                    PersonalAccountPermissionRequiredMixin,
                                    CreateView):
    template_name = 'create_personal_account.html'
    model = PersonalAccount
    form_class = AdminPersonalAccountForm
    success_message = 'Особовий рахунок успішно створено'
    # TODO: change to personal accounts list page
    success_url = reverse_lazy('adminlte_personal_account_create')

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")

        return super().form_invalid(form)


class AdminPersonalAccountFlatsView(PersonalAccountPermissionRequiredMixin,
                                    View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('section_id')
        flats = Flat.objects.filter(section=term, personalaccount__isnull=True).values('no', 'id')
        return JsonResponse(data=list(flats), safe=False)


class AdminPersonalAccountOwnerView(PersonalAccountPermissionRequiredMixin,
                                    View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('flat_id')
        owner = (Flat.objects.annotate(
            full_name=Concat('owner__last_name',
                             Value(' '),
                             'owner__first_name',
                             Value(' '),
                             'owner__middle_name'),
            phone=F('owner__phone_number')
        ).values('owner__pk', 'full_name', 'phone').get(pk=term))
        return JsonResponse(data=owner, safe=False)
