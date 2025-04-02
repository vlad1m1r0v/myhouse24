from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.authentication.models import CustomUser
from src.core.utils.permissions import OwnerRequiredMixin
from src.flat_owners.forms import AccountProfileForm


class AccountProfileUpdateView(
    SuccessMessageMixin,
    OwnerRequiredMixin,
    UpdateView
):
    template_name = 'flat_owners/account/update.html'
    model = CustomUser
    form_class = AccountProfileForm
    success_message = 'Дані користувача успішно оновлено'
    success_url = reverse_lazy('account:profile:index')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.instance)
        return response

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)


