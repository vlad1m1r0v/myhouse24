from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.cash_box.models import Transaction


class HouseUserRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # transaction id
        pk = kwargs.get('pk')

        message = "Ви не можете переглядати транзакцію"

        has_permission = (user.is_superuser or
                          Transaction.objects.filter(pk=pk, personal_account__house__users__in=[user.pk]).exists())

        if not has_permission:

            if is_ajax(request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(request, message)
            return redirect(reverse('adminlte:cash-box:list'))

        return super().dispatch(request, *args, **kwargs)
