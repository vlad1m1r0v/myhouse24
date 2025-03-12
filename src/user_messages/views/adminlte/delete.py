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
    # TODO: change to messages list page
    success_url = reverse_lazy('adminlte:messages:create')