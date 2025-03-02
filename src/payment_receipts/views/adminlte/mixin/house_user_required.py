from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.payment_receipts.models import Receipt


class HouseUserRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')

        message = "Ви не можете переглядати квитанцію"

        has_permission = (user.is_superuser or
                          Receipt.objects.filter(pk=pk, house__users__user__in=[request.user.id]).exists())

        if not has_permission:

            if is_ajax(request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(request, message)
            return redirect(reverse('adminlte:receipts:create'))

        return super().dispatch(request, *args, **kwargs)
