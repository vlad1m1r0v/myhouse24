from django import template

register = template.Library()


@register.inclusion_tag("personal_accounts/adminlte/_partials/balance.html")
def account_balance(obj):
    return {'object': obj}