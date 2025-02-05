from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.flats.models import Flat


class FlatUserRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')

        message = "У Вас немає доступу до квартири"

        has_permission = (user.is_superuser or
                          Flat.objects.filter(pk=pk, house__users__user__in=[request.user.id]).exists())

        if not has_permission:

            if is_ajax(request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(request, message)
            return redirect(reverse('adminlte:flats:list'))

        return super().dispatch(request, *args, **kwargs)
