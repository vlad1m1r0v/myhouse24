from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from src.website_management.forms import AdminMainPageSlideFormSet, AdminMainPageForm, AdminMainPageBlockFormSet
from src.website_management.models import MainPageSlide, MainPage, MainPageBlock


class AdminMainPageView(PermissionRequiredMixin, TemplateView):
    template_name = 'website_management/main_page.html'
    permission_required = ('authentication.website_management',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['slides'] = AdminMainPageSlideFormSet(
        queryset=MainPageSlide.objects.all(),
            prefix='slides',
        )

        (obj, _) = MainPage.objects.get_or_create(pk=1)
        context['main_page'] = AdminMainPageForm(instance=obj)

        context['blocks'] = AdminMainPageBlockFormSet(
            queryset=MainPageBlock.objects.all(),
            prefix='blocks',
        )

        return context

    def post(self,request, *args, **kwargs):
        slide_formset = AdminMainPageSlideFormSet(self.request.POST, self.request.FILES, prefix='slides')
        block_formset = AdminMainPageBlockFormSet(self.request.POST, self.request.FILES, prefix='blocks')
        page = AdminMainPageForm(self.request.POST, instance=MainPage.objects.first())
        if slide_formset.is_valid() and block_formset.is_valid() and page.is_valid():
            slide_formset.save()
            block_formset.save()
            page.save()
            messages.success(self.request, 'Домашня сторінка сайту успішно оновлена')
        else:
            for form_errors in block_formset.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)
        return redirect(reverse_lazy('adminlte_website_management_home'))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до управління cайтом')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))