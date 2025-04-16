from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from src.authentication.forms import AccountLoginForm
from src.authentication.models import CustomUser
from src.flats.models import Flat


def statistics_redirect(account_id: str):
    flat = Flat.objects.filter(owner=account_id).order_by('no').first()
    return f"{reverse_lazy('account:dashboard:index')}?flat_id={flat.id}"


class AccountLoginView(TemplateView):
    template_name = 'authentication/account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = AccountLoginForm()

        return context

    def dispatch(self, request, *args, **kwargs):
        account_id = request.GET.get('account_id')

        if account_id:
            referer = request.META.get('HTTP_REFERER')
            account_url = reverse_lazy('adminlte:flat-owners:detail', kwargs={'pk': account_id})
            from_account_url = referer == request.build_absolute_uri(account_url)

            if from_account_url:
                user = CustomUser.objects.get(pk=account_id)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Адміністратор успішно увійшов в особистий кабінет користувача')
                return redirect(statistics_redirect(account_id))

        if all([request.user.is_authenticated,
                not request.user.is_staff,
                not request.user.is_superuser]):
            return redirect(statistics_redirect(account_id))
        return super().dispatch(request, *args, **kwargs)

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
                return redirect(statistics_redirect(user.pk))

        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f"{error}")

            return redirect('authentication:account:login')
