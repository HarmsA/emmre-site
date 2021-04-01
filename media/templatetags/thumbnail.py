from django import template
register = template.Library()
from django.utils.html import mark_safe


@register.simple_tag
def thumbnail(img, max_width):
	return mark_safe(img.thumb(max_width=max_width))

