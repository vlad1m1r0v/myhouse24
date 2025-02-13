from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.authentication.models import CustomUser
'''
Only users who have access to an apartment belonging to its owner can view, update, and delete it
'''
class HouseUserRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        '''
        flat owner id
        '''
        pk = kwargs.get('pk')

        message = "Ви не можете переглядати інформацію цього власника квартири"

        has_permission = (user.is_superuser or
                          CustomUser.objects.filter(pk=pk, flats__house__users__user__in=[user.id]).exists())

        if not has_permission:

            if is_ajax(request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(request, message)
            return redirect(reverse('adminlte:flats-owners:list'))

        return super().dispatch(request, *args, **kwargs)