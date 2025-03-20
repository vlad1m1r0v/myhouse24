from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .mixin import PersonalAccountPermissionRequiredMixin
from ...forms import AdminPersonalAccountForm
from ...models import PersonalAccount


class AdminPersonaAccountUpdateView(SuccessMessageMixin,
                                    PersonalAccountPermissionRequiredMixin,
                                    UpdateView):
    template_name = 'personal_accounts/adminlte/update.html'
    model = PersonalAccount
    form_class = AdminPersonalAccountForm
    success_message = 'Особовий рахунок успішно оновлено'
    success_url = reverse_lazy('adminlte:personal-accounts:list')

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")

        return super().form_invalid(form)