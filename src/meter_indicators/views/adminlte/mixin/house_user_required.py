from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.core.utils import is_ajax
from src.meter_indicators.models import MeterIndicator


class HouseUserRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        message = "Ви не можете переглядати показники лічильників цієї квартири"

        user = self.request.user

        # Primary key of meter indicator record for detail, update, delete views
        pk = kwargs.get('pk')
        # Or flat id for list meter indicators view for flats
        flat_id = self.request.GET.get('flat_id')

        is_superuser = user.is_superuser
        is_houseuser = False

        if not is_superuser:
            if pk:
                is_houseuser = MeterIndicator.objects.filter(pk=pk, flat__house__users__user=user).exists()

            elif flat_id:
                is_houseuser = MeterIndicator.objects.filter(flat_id=flat_id, flat__house__users__user=user).exists()

        has_permission = is_superuser or is_houseuser

        if not has_permission:

            if is_ajax(self.request):
                return JsonResponse(status=403, data={'success': False, 'message': message})

            messages.error(self.request, message)
            return redirect(reverse('adminlte:meter-indicators:list'))

        return super().dispatch(self.request, *args, **kwargs)
