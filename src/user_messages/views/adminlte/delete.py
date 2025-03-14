from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from ...models import Message
from .mixin import (
    HouseUserRequiredMixin,
    MessagePermissionRequiredMixin
)


class AdminMessageDeleteView(
    SuccessMessageMixin,
    HouseUserRequiredMixin,
    MessagePermissionRequiredMixin,
    DeleteView
):
    model = Message
    success_message = 'Повідомлення успішно видалено'
    success_url = reverse_lazy('adminlte:messages:list')