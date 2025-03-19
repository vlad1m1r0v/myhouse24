from django import template

register = template.Library()


@register.inclusion_tag("personal_accounts/adminlte/_partials/status.html")
def account_status(obj):
    return {'object': obj}