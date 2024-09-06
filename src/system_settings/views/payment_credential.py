from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from src.system_settings.forms import AdminPaymentCredentialForm
from src.system_settings.models import PaymentCredential


class AdminPaymentCredentialView(SuccessMessageMixin, PermissionRequiredMixin, FormView):
    template_name = 'system_settings/payment_credential.html'
    form_class = AdminPaymentCredentialForm
    permission_required = ('authentication.payment_information',)
    success_url = reverse_lazy('adminlte_payment_credential')
    success_message = 'Платіжні реквізити успішно оновлено'

    def get_object(self):
        (obj, _) = PaymentCredential.objects.get_or_create(pk=1)
        return obj

    def get_form(self, form_class=None):
        instance = self.get_object()
        form_class = self.get_form_class()
        return form_class(instance=instance, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до платіжних реквізитів')
        return redirect(reverse('authentication_adminlte_login'))
