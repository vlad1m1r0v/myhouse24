from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy('authentication:account:login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Користувач успішно вийшов з системи")
        return response