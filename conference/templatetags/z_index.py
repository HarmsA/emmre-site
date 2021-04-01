from django import template
register = template.Library()
from writersdigest.settings import Z_INDEX_PRIORITIES

@register.simple_tag
def z_index(key):
	if not key in Z_INDEX_PRIORITIES:
		return 0
	return Z_INDEX_PRIORITIES.index(key) + 1

