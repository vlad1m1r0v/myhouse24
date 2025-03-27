from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.authentication.forms import AccountLoginForm


class AccountLoginView(TemplateView):
    template_name = 'authentication/account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = AccountLoginForm()

        return context

    def post(self, *args, **kwargs):
        form = AccountLoginForm(self.request.POST)

        if form.is_valid():
            user_login = form.cleaned_data['login']
            password = form.cleaned_data['password']

            user = authenticate(email=user_login, password=password)

            if user is None or user.is_staff or user.is_superuser:
                messages.error(self.request, 'Неправильний логін або пароль')
                return redirect('authentication:account:login')

            if not user.is_active:
                messages.error(self.request, 'Користувач не пройшов перевірку по E-Mail')
                return redirect('authentication:account:login')

            if user.status != 'active':
                messages.error(self.request, 'Акаунт не активовано адміністратором')
                return redirect('authentication:account:login')

            else:
                login(self.request, user)

                if not form.cleaned_data.get('remember_me'):
                    self.request.session.set_expiry(0)

                messages.success(self.request, 'Користувач успішно увійшов в систему')
                # TODO: change to first statistics page for account
                return redirect('authentication:account:login')

        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f"{error}")

            return redirect('authentication:account:login')


