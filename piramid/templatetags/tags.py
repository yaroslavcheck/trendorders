from django import template
from django.template.defaultfilters import stringfilter, floatformat

register = template.Library()


@register.filter
@floatformat
def round_float(s):
    return round(s, 2)
