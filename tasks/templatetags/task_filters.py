from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """Usage: {{ value|replace:"old:new" }} or {{ value|replace:"_: " }}"""
    if ':' in args:
        old, new = args.split(':', 1)
        return str(value).replace(old, new)
    return value
