from django.views.generic import TemplateView

from src.authentication.forms import AccountLoginForm


class AccountLoginView(TemplateView):
    template_name = 'authentication/account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = AccountLoginForm()

        return context