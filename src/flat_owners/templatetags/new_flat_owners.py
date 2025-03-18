from django import template
from src.authentication.models import CustomUser

register = template.Library()


@register.simple_tag
def new_flat_owners():
    qs = CustomUser.objects.filter(
        is_staff=False,
        is_superuser=False,
        status='new'
    )
    return {'total': qs.count(), 'qs': qs}
