from django import template
from django.template.defaultfilters import stringfilter, floatformat

register = template.Library()


@register.simple_tag
@stringfilter
def round_float(s: float):
    return round(s, 2)
