from django.views.generic import TemplateView


class AdminHouseOwnerCreateView(TemplateView):
    template_name = 'house_owners/create_house_owner.html'
