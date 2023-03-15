from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, view_name):
    return 'active' if context['nv'] == view_name else ''

# You can replace 'active' with any other class formatting, for example 'text-primary'