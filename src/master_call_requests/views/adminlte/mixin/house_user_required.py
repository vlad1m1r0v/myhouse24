from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.master_call_requests.models import MasterCallRequest


class HouseUserRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        message = "Ви не можете переглядати заявку виклику майстра цієї квартири"

        user = self.request.user

        pk = kwargs.get('pk')

        is_superuser = user.is_superuser
        is_houseuser = False

        if not is_superuser:

            if pk:
                is_houseuser = MasterCallRequest.objects.filter(pk=pk, flat__house__users__user=user).exists()

        has_permission = is_superuser or is_houseuser

        if not has_permission:

            if is_ajax(self.request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(self.request, message)
            return redirect(reverse('adminlte:master-call-requests:list'))

        return super().dispatch(self.request, *args, **kwargs)
