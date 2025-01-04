from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import View
from django.shortcuts import redirect


class AuthenticationAdminLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, f'Користувач  успішно вийшов із системи')
        return redirect(reverse_lazy('authentication:adminlte:login'))
