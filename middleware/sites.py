from conference.models import Site
from django.core.exceptions import ObjectDoesNotExist
try:
	from urllib.parse import urlparse
except:
	from urlparse import urlparse

class SimpleMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		parse_object = urlparse(request.build_absolute_uri())
		hostname = parse_object.netloc
		if ":" in hostname:
			hostname = hostname.rsplit(':', 1)[0]

		hostname = hostname.replace('local.', '')

		try:
			request.site = Site.objects.get(domain=hostname)
		except ObjectDoesNotExist:
			request.site = Site.objects.get(domain='writersdigestconference.com')
		except:
			request.site = None

		response = self.get_response(request)
		# raise Exception(request.site)
		return response

