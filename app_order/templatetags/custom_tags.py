import roman
from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now

register = template.Library()


@register.filter
def repeat(value, count):
    return value * count


@register.filter
def romanize(value):
    try:
        return roman.toRoman(int(value))
    except (ValueError, TypeError, roman.InvalidRomanNumeralError):
        return value


@register.filter
def timeago(value):
    if not value:
        return ""
    diff = timesince(value, now())

    return f"{diff.split(',')[0]} ago"


@register.filter
def rep_icon(score):
    if score < 0:
        return 'media/rep-icon-low.png'
    elif score <= 10:
        return 'media/rep-icon-normal.png'
    else:
        return 'media/rep-icon-high.png'


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.simple_tag(takes_context=True)
def querystring_with(context, **kwargs):
    """Merges request.GET with new values in kwargs."""
    request = context['request']
    current = request.GET.copy()

    for key, value in kwargs.items():
        if value is None:
            current.pop(key, None)
        else:
            current[key] = value

    return '?' + current.urlencode()
