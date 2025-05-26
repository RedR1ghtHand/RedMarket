from django import template
import roman

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