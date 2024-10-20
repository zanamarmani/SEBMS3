# In your app's templatetags directory, create a file named 'menu_tags.py'

from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def set_active(context, url_name):
    request = context['request']
    return 'active' if request.path == request.build_absolute_uri(reverse(url_name)) else ''
