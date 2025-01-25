from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.houses.models import House


class HouseUserRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')

        message = "У Вас немає доступу до будинку"

        has_permission = user.is_superuser or House.objects.filter(pk=pk, users__user=user).exists()

        if not has_permission:

            if is_ajax(request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(request, message)
            return redirect(reverse('adminlte:houses:list'))

        return super().dispatch(request, *args, **kwargs)
