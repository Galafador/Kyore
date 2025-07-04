from django import template
from django.utils.safestring import mark_safe
register = template.Library()

SUPERSCRIPT_FONT_SIZE = 1

def split_decimal(value):
    """
    Helper function to split float input value into int and decimal parts as string
    """
    int_part, dec_part = str(value).split(".")
    dec_part = dec_part.rstrip("0")
    return int_part, dec_part

@register.filter
def format_decimal_to_superscript(value):
    """
    convert decimal part of a value into superscript
    Example: 123.45 --> 123<sup>.45</sup>
    """
    try:
        int_part, dec_part = split_decimal(value)
        if dec_part:
            return mark_safe(f'{int_part}<sup style="font-size: {SUPERSCRIPT_FONT_SIZE}rem">.{dec_part}</sup>')
        else:
            return str(int_part)
    except (ValueError, TypeError):
        return str(value)

def format_thousands_suffix(value, args, use_superscript):
    """
    helper function to format values with K(Thousands)/M(Millions)/B(Billions)/T(Trillions)
    and optional supercript for the decimal place
    """
    try:
        value = float(value)
        if value >= 1000_000_000_000:
            val = value/1000_000_000_000
            suffix = "T"
        elif value >= 1000_000_000:
            val = value/1000_000_000
            suffix = "B"
        elif value >= 1000_000:
            val = value/1000_000
            suffix = "M"
        elif value >= 1000:
            val = value/1000
            suffix = "K"
        else:
            return format_decimal_to_superscript(value) if use_superscript else f"{value:.{args}f}"
        
        val_str = f"{val:.{args}f}"
        if use_superscript:
            val_str = format_decimal_to_superscript(val_str)
            return mark_safe(f"{val_str} {suffix}")
        else:
            return mark_safe(f"{val_str} {suffix}")
    except(ValueError, TypeError):
        return str(value)

@register.filter
def format_thousands_then_superscript (value, args=0):
    """
    format values into K(Thousands)/M(Millions)/B(Billions)/T(Trillions) with decimal part as superscript
    """
    return format_thousands_suffix(value, args, use_superscript=True)

@register.filter
def format_thousands (value, args=0):
    """
    format values into K(Thousands)/M(Millions)/B(Billions)/T(Trillions) without decimal part as superscript
    """
    return format_thousands_suffix(value, args, use_superscript=False)