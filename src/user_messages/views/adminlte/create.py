from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from openpyxl.pivot.fields import Boolean

from src.authentication.models import CustomUser
from .mixin import MessagePermissionRequiredMixin
from ...forms import AdminMessageForm
from ...models import Message


class AdminMessageCreateView(
    SuccessMessageMixin,
    MessagePermissionRequiredMixin,
    CreateView):
    success_message = 'Повідомлення успішно створено'
    success_url = reverse_lazy('adminlte:messages:list')
    model = Message
    form_class = AdminMessageForm
    template_name = 'user_messages/adminlte/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        initial = {}

        user = self.request.user
        to_debtors = self.request.GET.get('to_debtors')
        owner_id = self.request.GET.get('owner_id')

        initial['creator'] = user

        initial['to_debtors'] = bool(to_debtors)

        if owner_id:
            owner = CustomUser.objects.get(id=owner_id)
            initial['flat_owner'] = owner


        kwargs['initial'] = initial

        return kwargs