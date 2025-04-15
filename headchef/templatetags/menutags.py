from django import template

register = template.Library()

@register.filter
def format_dish_name(value):
    ''' Custom Filter to format dish name in Django templates'''
    return ' '.join([i.capitalize() for i in value.split('_')])
