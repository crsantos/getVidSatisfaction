from django import template
register = template.Library()
 
@register.filter("slugify")
def slugify(value):
    return value.replace(' ','_')