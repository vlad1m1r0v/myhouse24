from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from src.payment_receipts.forms import AdminReceiptTemplateUploadForm
from src.payment_receipts.models import ReceiptTemplate
from src.payment_receipts.views.adminlte.mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsTemplateSettingsView(
    ReceiptsPermissionRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/adminlte/template_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = AdminReceiptTemplateUploadForm()

        context['templates'] = ReceiptTemplate.objects.all()

        return context

    def post(self, *args, **kwargs):
        form = AdminReceiptTemplateUploadForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            form.save()
            messages.success(self.request, 'Шаблон успішно завантажено')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(self.request, error)

        return redirect('adminlte:receipts:templates:index')
