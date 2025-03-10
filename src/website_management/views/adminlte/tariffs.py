from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from src.website_management.forms import AdminTariffsPageForm, AdminTariffsPageBlockFormSet
from src.website_management.models import TariffsPage, TariffsPageBlock
from .mixin import WebsitePermissionRequiredMixin

class AdminTariffsPageView(WebsitePermissionRequiredMixin,
                           TemplateView):
    template_name = 'website_management/adminlte/tariffs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        (obj,_) = TariffsPage.objects.get_or_create(pk=1)
        context['page'] = AdminTariffsPageForm(instance=obj)

        context['tariffs']  =AdminTariffsPageBlockFormSet(
            queryset=TariffsPageBlock.objects.all(),
        )

        return context

    def post(self,request, *args, **kwargs):
        form = AdminTariffsPageForm(request.POST, instance=TariffsPage.objects.first())
        tariffs = AdminTariffsPageBlockFormSet(request.POST, request.FILES)

        if form.is_valid() and tariffs.is_valid():
            form.save()
            tariffs.save()
            messages.success(request, 'Сторінка "Тарифи" успішно оновлена')
        else:
            for form_errors in tariffs.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)
        return redirect(reverse_lazy('adminlte:website-management:tariffs'))