from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View
from django.shortcuts import redirect
from .forms import AdminLoginForm


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
            'authentication.roles': reverse('adminlte_permissions'),
            'authentication.users': reverse('adminlte_users_list'),
            'authentication.payment_information': reverse('adminlte_payment_credential'),
            'authentication.payment_items': reverse('adminlte_payment_items_list')
        }

        for perm, url in permission_to_url.items():
            if self.request.user.has_perm(f'{perm}'):
                messages.success(self.request, 'Адміністратор успішно увійшов в систему')
                return url

        messages.error(self.request, 'В адміністратора немає права доступу до жодної зі сторінок')
        return reverse('authentication_adminlte_login')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AuthenticationAdminLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Адміністратор  успішно вийшов із системи')
        return redirect(reverse_lazy('authentication_adminlte_login'))
