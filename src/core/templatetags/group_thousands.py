from django import template

register = template.Library()

@register.filter
def group_thousands(value):
    try:
        value = float(value)
        integer_part, decimal_part = f"{value:.10f}".rstrip("0").split(".")
        formatted_integer = f"{int(integer_part):,}".replace(",", " ")
        return f"{formatted_integer}.{decimal_part}" if decimal_part else formatted_integer
    except (ValueError, TypeError):
        return value