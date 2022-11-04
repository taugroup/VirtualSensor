# Usage: <li><a class="{% active request '^/contact' %}" href="/contact">Contact</a></li>
from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''
