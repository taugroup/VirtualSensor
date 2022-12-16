from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter
@stringfilter
def csvfields(inputstr):
    ret_str = ''
    import ast
    str_list = ast.literal_eval(inputstr)
    for s in str_list:
        ret_str += "<span class='badge badge-pill badge-primary'>"+s+"</span>"
    return ret_str