from django import template

from src.website_management.models import ContactsPage

register = template.Library()


@register.inclusion_tag("website_management/website/_partials/contacts.html")
def contacts():
    return {
        'contacts': ContactsPage.objects.values('name', 'location', 'address', 'phone', 'email').first()
    }
