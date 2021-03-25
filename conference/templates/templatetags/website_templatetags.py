from django import template
register = template.Library()
import re
from django.utils.html import format_html
from writersdigest.settings import BASE_DIR

import os
import requests
import datetime, pytz, time
from writersdigest.settings import SCRIPT_CACHE_TIME, STYLE_CACHE_TIME, DEBUG, STAGE

import hashlib

def hash_names(names):
	return hashlib.md5(names.encode('utf-8')).hexdigest()[:9]

@register.filter
def site_variable(value, arg):
	site = Site.get_site_from_host(value, database=False)
	response = ""
	if site and arg in site.data:
		args = arg.split('.')
		response = site
		for arg in args:
			response = response[arg]
	return response


@register.simple_tag
def combine_scripts(request, scripts, asynchronous=False, defer=False):
	name = hash_names(scripts) + ".js"
	relative_directory = "/assets/js/cache/"
	relative_path = relative_directory + name
	absolute_directory = BASE_DIR.rstrip('/') + relative_directory
	cached_path = absolute_directory + name

	if not os.path.exists(absolute_directory):
		os.makedirs(absolute_directory)

	cached = os.path.isfile(cached_path)
	age = None

	if cached:
		timestamp = datetime.datetime.fromtimestamp(os.stat(cached_path).st_mtime)
		age = datetime.datetime.now() - timestamp

	if not cached or age > datetime.timedelta(minutes=SCRIPT_CACHE_TIME):

		scripts = scripts.split(", ")

		combined_scripts = ""

		for script in scripts:
			script = script.strip()
			if script.startswith('/') and not script.startswith('//'):
				try:
					file = open(BASE_DIR.rstrip('/') + script, r'r', encoding="utf-8")
					combined_scripts += str(file.read()) + str("\n\n\n\n")
					file.close()
				except:
					if DEBUG:
						raise Exception(script)
					continue
			elif STAGE == 'local':
				continue
			else:

				r = None
				if DEBUG:
					r = requests.get(request.build_absolute_uri(script), verify=False, allow_redirects=False, timeout=5)
				else:
					try:
						r = requests.get(request.build_absolute_uri(script), verify=False, allow_redirects=False, timeout=5)
					except:
						continue

				if r and r.status_code == 200:
					combined_scripts += str(r.text) + str("\n\n\n\n")

		combined_scripts = combined_scripts.replace('"use strict"', '')

		try:
			file = open(cached_path, r'w+', encoding="utf-8")
			file.write(combined_scripts)
			file.close()
		except Exception as e:
			print("Cannot cache js file: invalid path: {path}.  Exception: {exception}".format(path=cached_path, exception=str(e)))

	asynchronous = "asynchronous" if asynchronous else ""
	defer = "defer" if defer else ""

	html = "<script src='{src}' type='text/javascript' {asynchronous} {defer}></script>".format(src=relative_path, asynchronous=asynchronous, defer=defer)
	return format_html(html)


@register.simple_tag
def combine_styles(request, styles):
	name = hash_names(styles) + ".css"
	relative_directory = "/assets/css/cache/"
	relative_path = relative_directory + name
	absolute_directory = BASE_DIR.rstrip('/') + relative_directory
	cached_path = absolute_directory + name

	if not os.path.exists(absolute_directory):
		os.makedirs(absolute_directory)

	cached = os.path.isfile(cached_path)
	age = None

	if cached:
		timestamp = datetime.datetime.fromtimestamp(os.stat(cached_path).st_mtime)
		age = datetime.datetime.now() - timestamp

	if not cached or age > datetime.timedelta(minutes=STYLE_CACHE_TIME):

		styles = styles.split(", ")

		combined_styles = ""

		for style in styles:
			style = style.strip()
			if style.startswith('/'):
				try:
					file = open(BASE_DIR.rstrip('/') + style, r'r', encoding="utf-8")
					combined_styles += str(file.read()) + str("\n\n\n\n")
					file.close()
				except:
					continue
			elif STAGE == 'local':
				continue
			else:
				try:
					r = requests.get(request.build_absolute_uri(style), verify=False, allow_redirects=False, timeout=1)
				except:
					continue
				if r and r.status_code == 200:
					combined_styles += str(r.text) + str("\n\n\n\n")

		try:
			file = open(cached_path, r'w+', encoding="utf-8")
			file.write(combined_styles)
			file.close()
		except Exception as e:
			print("Cannot cache css file: invalid path: {path}.  Exception: {exception}".format(path=cached_path, exception=str(e)))

	return format_html("<link href='{href}' rel='stylesheet'>".format(href=relative_path))


@register.simple_tag
def replace(string, old, new):
	return string.replace(old, new)