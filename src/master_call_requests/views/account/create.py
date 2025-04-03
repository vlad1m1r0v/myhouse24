from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from src.core.utils.permissions import OwnerRequiredMixin
from src.master_call_requests.forms import AccountMasterCallRequestForm
from src.master_call_requests.models import MasterCallRequest


class AccountMasterCallRequestCreateView(
    OwnerRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'master_call_requests/account/create.html'
    model = MasterCallRequest
    success_message = 'Заявку виклику майстра успішно створено'
    success_url = reverse_lazy('account:master-call-requests:list')
    form_class = AccountMasterCallRequestForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.flat_owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")

        return super().form_invalid(form)

