from django import template

register = template.Library()


@register.filter
def times(value):
    return range(value)


@register.filter
def remaining_stars(value):
    return range(5 - value)
