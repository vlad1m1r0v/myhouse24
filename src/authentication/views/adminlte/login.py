from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import FormView
from django.shortcuts import redirect
from src.authentication.forms import AdminLoginForm


class AuthenticationAdminLoginView(FormView):
    form_class = AdminLoginForm
    template_name = 'authentication/adminlte/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.get_all_permissions():
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(email=email, password=password, is_superuser=True)

        if user:
            login(self.request, user)
            redirect_url = self.get_success_url()

            if not form.cleaned_data.get('remember_me'):
                self.request.session.set_expiry(0)

            return redirect(redirect_url)

        messages.error(self.request, 'Неправильний логін або пароль')

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        permission_to_url = {
            'authentication.houses': reverse('adminlte:houses:list'),
            'authentication.meter_indicators': reverse('adminlte:meter-indicators:list'),
            'authentication.website_management': reverse('adminlte:website-management:home'),
            'authentication.services': reverse('adminlte:system-settings:services:index'),
            'authentication.roles': reverse('adminlte:system-settings:permissions:index'),
            'authentication.users': reverse('adminlte:system-settings:users:list'),
            'authentication.payment_information': reverse('adminlte:system-settings:payment-credential:index'),
            'authentication.payment_items': reverse('adminlte:system-settings:payment-items:list'),
        }


        if self.request.user.is_superuser:
            messages.success(self.request, 'Користувач успішно увійшов в систему')
            return permission_to_url[next(iter(permission_to_url))]

        for perm, url in permission_to_url.items():
            if self.request.user.has_perm(f'{perm}'):
                messages.success(self.request, 'Користувач успішно увійшов в систему')
                return url

        messages.error(self.request, 'В користувача немає права доступу до жодної зі сторінок')
        return reverse('authentication:adminlte:login')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))