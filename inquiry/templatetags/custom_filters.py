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


@register.filter
def changed_type(value:str):
    if value == "deposit":
        return "입금"
    elif value == "withdraw":
        return "출금"
    else:
        return "기타"
