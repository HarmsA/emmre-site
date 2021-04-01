from django.shortcuts import render

import os, requests, urllib3
from PIL import Image as PILImage
from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, Http404
from django.views.decorators.http import require_safe, require_POST, require_GET, require_http_methods
from django.core.cache import caches
from django.views.decorators.cache import cache_page

from media.models import *
from media.forms import *

cache = caches['filesystem']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# @require_safe
# @cache_page(60*60*24*7)
# def image(request, id):
#
# 	image = Image.objects.get(id=id)
# 	if not image:
# 		raise Http404()
#
# 	response = render(request, "image.html", {
# 		"image": image,
# 	})
# 	response['X-Robots-Tag'] = "none"
# 	return response


# @require_GET
# @cache_page(60*60*24*7)
# def image_proxy(request, id):
#
# 	image = Image.objects.get(id=id)
# 	if not image:
# 		raise Http404()
#
# 	key = "proxy_{image_id}".format(image_id=image.id)
# 	response = cache.get(key)
# 	if response:
# 		return response
#
# 	r = None
#
# 	try:
# 		r = requests.get(image.url, timeout=2, verify=False, allow_redirects=True)
# 	except:
# 		pass
#
# 	if not r:
# 		return HttpResponse("", status=404)
#
# 	content_type = "application/octet-stream"
# 	if hasattr(r, 'headers') and 'content-type' in r.headers:
# 		content_type = r.headers['content-type']
#
# 	response = HttpResponse(r.content, status=r.status_code, content_type=content_type)
#
# 	response['X-Robots-Tag'] = "none"
# 	cache.set(key, response, 60*60*24*7)
# 	return response


@require_GET
# @cache_page(60*60*24*7)
def image_thumbnail(request, id):

	image = Image.objects.get(id=id)
	if not image:
		raise Http404()

	form = ImageThumbnailForm(request.GET)
	if not form.is_valid():
		return HttpResponse("", status=400)

	max_width = form.cleaned_data.get('max_width')
	max_height = form.cleaned_data.get('max_height')

	key = "thumb_{image_id}_{max_width}_{max_height}".format(
		image_id = image.id,
		max_width = max_width if max_width else '',
		max_height = max_height if max_height else '',
	)
	response = cache.get(key)
	if response:
		return response

	r = None

	r = requests.get(image.url)

	if not r:
		return HttpResponse("", status=404)
	# raise Exception(r.headers)
	# content_type = dict(r.items()).get('Content-Type')
	content_type = r.headers['content-type']
	# raise Exception(content_type)
	pil_formats = {
		"image/jpg": "jpeg",
		"image/jpeg": "jpeg",
		"image/png": "png",
	}
	pil_format = pil_formats.get(content_type)
	if not pil_format:
		return HttpResponse("", status=400)

	im = PILImage.open(BytesIO(r.content))
	current_width, current_height = im.size
	if max_width or max_height:
		if max_width and not max_height:
			max_height = round(current_height * max_width/current_width)
		elif max_height and not max_width:
			max_width = round(current_width * max_height/current_height)
		im.thumbnail((max_width, max_height))
	temp = BytesIO()
	im.save(temp, format=pil_format)

	response = HttpResponse(temp.getvalue(), status=r.status_code, content_type=content_type)

	response['X-Robots-Tag'] = "none"
	cache.set(key, response, 60*60*24*7)
	return response