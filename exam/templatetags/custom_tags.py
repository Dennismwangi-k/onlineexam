from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def is_active(request, view_name):
    url = reverse(view_name)
    return "active" if request.path == url else ""
