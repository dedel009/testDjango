from django import template

register = template.Library()


@register.filter
def intcomma(value):
    if isinstance(value, int):
        return f"{value:,}"
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value