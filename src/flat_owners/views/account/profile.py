from django.views.generic import TemplateView


class AccountProfileView(TemplateView):
    template_name = 'flat_owners/account/profile.html'