from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.user_messages.models import Message


class HouseUserRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # message id
        pk = kwargs.get('pk')

        message = "Ви не можете переглядати повідомлення"

        has_permission = (user.is_superuser or
                          Message.objects.filter(pk=pk, house__users__user__in=[user.pk]).exists())

        if not has_permission:

            if is_ajax(request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(request, message)
            return redirect(reverse('adminlte:messages:list'))

        return super().dispatch(request, *args, **kwargs)