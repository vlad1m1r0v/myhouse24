from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.personal_accounts.models import PersonalAccount
from .mixin import FlatPermissionRequiredMixin
from ...forms.adminlte.house import AdminFlatForm


class AdminFlatCreateView(FlatPermissionRequiredMixin,
                          CreateView):
    template_name = 'flats/adminlte/create.html'
    form_class = AdminFlatForm
    # TODO: change to flats list page URL
    success_url = reverse_lazy('adminlte:flats:create')

    def form_valid(self, form):
        new_personal_account = form.cleaned_data.get('new_personal_account')
        personal_account = form.cleaned_data.get('personal_account')

        flat = form.save()

        if new_personal_account:
            personal_account = PersonalAccount.objects.create(
                no=new_personal_account,
                house=form.cleaned_data.get('house'),
                section=form.cleaned_data.get('section'),
                flat=flat
            )

            personal_account.save()

        elif personal_account:
            try:
                personal_account.flat = flat
                personal_account.save()
            except PersonalAccount.DoesNotExist:
                messages.error(self.request, 'Особовий рахунок не знайдено')

        messages.success(self.request, 'Нову квартиру успішно створено')
        # TODO: depending on submit button name we should redirect either to "create flat" URL or "flats list" URL
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")

        return super().form_invalid(form)
