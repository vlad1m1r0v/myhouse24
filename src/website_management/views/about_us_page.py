from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from src.website_management.forms import AdminAboutUsGalleryFormSet, AdminAboutUsDocumentFormSet, \
    AdminAboutUsPageForm, AdminAboutUsAdditionalGalleryFormSet
from src.website_management.models import AboutUsPage, AboutUsGallery, AboutUsAdditionalGallery, AboutUsDocument


class AdminAboutUsPageView(PermissionRequiredMixin, TemplateView):
    template_name = 'website_management/about_us_page.html'
    permission_required = ('authentication.website_management',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        (obj, _) = AboutUsPage.objects.get_or_create(pk=1)

        context['about_us'] = AdminAboutUsPageForm(
            instance=obj
        )

        context['gallery'] = AdminAboutUsGalleryFormSet(
            queryset=AboutUsGallery.objects.all(),
            prefix='gallery',
        )

        context['documents'] = AdminAboutUsDocumentFormSet(
            queryset=AboutUsDocument.objects.all(),
            prefix='document',
        )

        context['additional_gallery'] = AdminAboutUsAdditionalGalleryFormSet(
            queryset=AboutUsAdditionalGallery.objects.all(),
            prefix='additional_gallery',
        )

        return context

    def post(self, *args, **kwargs):
        page_form = AdminAboutUsPageForm(
            self.request.POST,
            self.request.FILES,
            instance=AboutUsPage.objects.first()
        )

        gallery_formset = AdminAboutUsGalleryFormSet(
            self.request.POST,
            self.request.FILES,
            prefix='gallery'
        )

        additional_gallery_formset = AdminAboutUsAdditionalGalleryFormSet(
            self.request.POST,
            self.request.FILES,
            prefix='additional_gallery'
        )

        document_formset = AdminAboutUsDocumentFormSet(
            self.request.POST,
            self.request.FILES,
            prefix='document'
        )

        if (page_form.is_valid()
                and gallery_formset.is_valid()
                and additional_gallery_formset.is_valid()
                and document_formset.is_valid()):

            page_form.save()
            gallery_formset.save()
            additional_gallery_formset.save()
            document_formset.save()

            messages.success(self.request, 'Сторінка "Про нас" успішно оновлена')
        else:
            messages.error(self.request, 'Виникли певні помилки про оновленні сторінки "Про нас"')
        return redirect(reverse_lazy('adminlte_website_management_about_us'))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до управління cайтом')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))
