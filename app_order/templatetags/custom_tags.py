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
    if score:
        if int(score) < 0:
            return 'media/rep-icon-low.png'
        elif int(score) <= 10:
            return 'media/rep-icon-normal.png'
        else:
            return 'media/rep-icon-high.png'
    else:
        return 'media/rep-icon-normal.png'


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
