from django import template
from django.urls import reverse # Import reverse to resolve the name

register = template.Library()


@register.inclusion_tag('trainer/components/_process_header.html')
def render_process_header(title, url_name=None):
    # keep params in simpler
    back_url = reverse(url_name) if url_name else None

    return {'title': title, 'back_url': back_url}