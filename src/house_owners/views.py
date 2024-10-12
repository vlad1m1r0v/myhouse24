from django.views.generic import CreateView

from src.house_owners.forms import AdminHouseOwnerForm


class AdminHouseOwnerCreateView(CreateView):
    template_name = 'house_owners/create_house_owner.html'
    form_class = AdminHouseOwnerForm
