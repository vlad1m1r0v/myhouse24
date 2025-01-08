from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from src.core.utils import CustomPermissionRequiredMixin
from src.system_settings.forms import AdminPaymentCredentialForm
from src.system_settings.models import PaymentCredential

class PaymentCredentialPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.payment_information'
    permission_denied_message = 'У Вас немає доступу до платіжних реквізитів'

class AdminPaymentCredentialView(
    SuccessMessageMixin,
    PaymentCredentialPermissionRequiredMixin,
    FormView):
    template_name = 'system_settings/adminlte/payment_credential.html'
    form_class = AdminPaymentCredentialForm
    success_url = reverse_lazy('adminlte:system-settings:payment-credential:index')
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
