from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .mixin import MessagePermissionRequiredMixin
from ...forms import AdminMessageForm
from ...models import Message


class AdminMessageCreateView(
    SuccessMessageMixin,
    MessagePermissionRequiredMixin,
    CreateView):
    success_message = 'Повідомлення успішно створено'
    # TODO: change to message list page
    success_url = reverse_lazy('adminlte:messages:create')
    model = Message
    form_class = AdminMessageForm
    template_name = 'user_messages/adminlte/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user = self.request.user

        kwargs['initial'] = {
            'creator': user,
        }

        return kwargs