from django import template

register = template.Library()


@register.filter("custom_slice", is_safe=True)
def slice_filter(value, arg):
    try:
        res = value[arg - 6: arg + 5]
        return res
    except (ValueError, TypeError):
        return value  # Fail silently.
