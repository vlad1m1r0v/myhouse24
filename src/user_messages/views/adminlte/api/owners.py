from django.db.models import Value, Q, Prefetch
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.authentication.models import CustomUser
from src.flats.models import Flat
from ..mixin import MessagePermissionRequiredMixin


class AdminMessagesOwnersView(MessagePermissionRequiredMixin,
                              View):
    def get(self, *args, **kwargs):
        user = self.request.user

        term = self.request.GET.get('term', '')

        filters = Q()

        filters &= Q(is_staff=False) & Q(is_superuser=False) & Q(status='active')

        if term:
            filters &= Q(text__icontains=term)

        if not user.is_superuser:
            filters &= Q(flat__house__users__in=[user.id])

        owners = (CustomUser.objects
                  .prefetch_related(Prefetch('flats', queryset=Flat.objects.select_related('house__users')))
                  .annotate(text=Concat('first_name', Value(' '), 'last_name'))
                  .filter(filters).values('text', 'id'))

        return JsonResponse(data=list(owners), safe=False)
