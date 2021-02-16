from config.models import *
from django.core.cache import cache
import json

def configuration_context_processor(request):

	cache_key = Setting.context_cache_key(site=request.site)
	settings = cache.get(cache_key)

	if settings:
		settings = json.loads(settings)
	else:
		settings = Setting.context(site=request.site)
		# raise Exception(settings)
		cache.set(key=cache_key, value=json.dumps(settings), timeout=3600, version=1)

	return {
		"settings": settings,
	}