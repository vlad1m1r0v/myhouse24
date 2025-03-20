from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .mixin import PersonalAccountPermissionRequiredMixin
from ...forms import AdminPersonalAccountForm
from ...models import PersonalAccount


class AdminPersonaAccountCreateView(SuccessMessageMixin,
                                    PersonalAccountPermissionRequiredMixin,
                                    CreateView):
    template_name = 'personal_accounts/adminlte/create.html'
    model = PersonalAccount
    form_class = AdminPersonalAccountForm
    success_message = 'Особовий рахунок успішно створено'
    success_url = reverse_lazy('adminlte:personal-accounts:list')

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")

        return super().form_invalid(form)