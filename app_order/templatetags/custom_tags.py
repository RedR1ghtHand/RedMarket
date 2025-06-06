from django import template
import roman
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
