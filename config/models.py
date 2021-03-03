from django.db import models
# from cuisine.site.managers import Manager
from django.db.models import Q
from django.utils.text import slugify
from django.utils.html import escape
from django.core.cache import cache
import json
from media.models import Image
from django.utils.safestring import mark_safe
import datetime
from functools import lru_cache
from django.template import Context, Template, RequestContext
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import mark_safe
from conference.models import Site



class SettingFolder(models.Model):

	def __unicode__(self):
		return str(self.get_path())
	def __str__(self):
		return str(self.get_path())

	class Meta:
		verbose_name = "Setting Folder"
		verbose_name_plural = "Setting Folders"
		managed = True
		# ordering = ['name']
		order_with_respect_to = 'parent'
		unique_together = (
			("parent", "name"),
		)

	# objects = Manager()

	id = models.AutoField(primary_key=True, null=False, blank=False, editable=False, db_column='id')
	name = models.SlugField(max_length=255, null=False, blank=False, unique=False)
	parent = models.ForeignKey('self', null=True, blank=True, db_column="parent", related_name="children", on_delete=models.SET_NULL)

	def get_path(self):
		path = ""
		if self.parent:
			path = "{path}".format(path=self.parent.get_path().strip('.'))
		path = "{path}.{name}".format(path=path.strip('.'), name=self.name.strip('.')).lower()
		path = path.lstrip('.')
		return path

	def save(self, request=None, *args, **kwargs):
		if self.name:
			self.name = slugify(self.name).replace("-", "_")
		super(SettingFolder, self).save(*args, **kwargs)

	def delete(self, request=None, *args, **kwargs):
		super(SettingFolder, self).delete(*args, **kwargs)


class Setting(models.Model):

	def __init__(self, *args, **kwargs):
		super(Setting, self).__init__(*args, **kwargs)
		self.original = {
			"value": self.value,
		}

	def __unicode__(self):
		return str(self.path())
	def __str__(self):
		return str(self.path())

	class Meta:
		verbose_name = "Setting"
		verbose_name_plural = "Settings"
		managed = True
		order_with_respect_to = 'folder'
		# ordering = ['folder__name', 'key']

	# objects = Manager()

	types = (
		("text", "Text"),
		("boolean", "Boolean"),
		("color", "Color"),
		("date", "Date"),
		("time", "Time"),
		("datetime", "Datetime"),
		("email", "Email"),
		("image", "Image"),
		# ("video", "Video"),
		("integer", "Integer"),
		("number", "Number"),
		("phone", "Phone"),
		("url", "Url"),
		("html", "Html"),
		("javascript", "Javascript"),
		("css", "CSS"),
	)

	id = models.AutoField(primary_key=True, null=False, blank=False, editable=False, db_column='id')
	key = models.SlugField(max_length=255, null=False, blank=False, unique=False, verbose_name='Field Title')
	value = models.TextField(null=True, blank=True, verbose_name="Content Field")
	folder = models.ForeignKey(SettingFolder, null=True, blank=True, db_column="folder", related_name="settings", on_delete=models.SET_NULL)
	type = models.CharField(max_length=255, null=True, blank=True, choices=types, default=types[0])
	site = models.ForeignKey(Site, null=True, blank=True, related_name='Settings', on_delete=models.CASCADE)

	def path(self):
		path = ""
		if self.folder:
			path = self.folder.get_path()
		path = "{path}.{key}".format(path=path.strip('.'), key=self.key.strip('.')).rstrip('.')
		path = path.lstrip('.')
		return path

	def render(self, context={}):

		assert isinstance(context, dict) or context is None

		value = self.value

		if self.type == 'image':
			image = Image.objects.get(id=value)
			value = {}
			if image:
				value = {
					"id": image.id,
					"url": image.url,
				}
		# elif self.type == 'video':
		# 	video = Video.objects.get(id=value)
		# 	value = {}
		# 	if video:
		# 		value = {
		# 			"id": video.id,
		# 			"source": video.source,
		# 			"poster": video.poster,
		# 			"youtube_id": video.youtube_id,
		# 		}

		return value

	@classmethod
	def context(cls, site=None):

		all_settings = cls.objects.all().select_related('folder')
		if site:
			all_settings = all_settings.filter(Q(site__isnull=True)|Q(site=site))
		folders = SettingFolder.objects.all().values("id", "parent_id", "name")
		progenitor_folders = []

		for folder in folders:
			if folder['parent_id']:
				continue
			progenitor_folders.append(folder)

		def get_settings_tree(folder=None):
			tree = {}
			for setting in all_settings:
				if not folder and setting.folder:
					continue
				if folder and not setting.folder:
					continue
				if folder and setting.folder and setting.folder.id != folder['id']:
					continue
				value = setting.render()
				if setting.key in tree:
					if not isinstance(tree[setting.key], list):
						tree[setting.key] = [tree[setting.key]]
					if isinstance(tree[setting.key], list):
						tree[setting.key].append(value)
				else:
					tree[setting.key] = value

			if folder:
				for child in folders:
					if child['parent_id'] != folder['id']:
						continue
					tree[child['name']] = get_settings_tree(folder=child)

			return tree

		tree = get_settings_tree()
		for folder in progenitor_folders:
			tree[folder['name']] = get_settings_tree(folder=folder)

		return tree

	@staticmethod
	def context_cache_key(site):
		if site:
			return 'settings_' + str(site.id)
		else:
			return 'setting_generic'

	@classmethod
	@lru_cache(maxsize=None, typed=False)
	def get(cls, path, site=None, **context):
		keys = path.split(".")
		value = cls.context(site=site)
		if not value:
			return None
		for key in keys:
			if not key in value:
				value = None
				break
			value = value[key]
		if context:
			try:
				value = value.format(**context)
			except:
				pass
		return value

	def preview(self, version=None):
		if not self.pk:
			return ""
		preview = ""
		value = self.value
		if version:
			value = version.value
		if self.type == 'color':
			preview = "<div style='width:50px;height:50px;background-color:{color};'></div>".format(color=value)
		# elif self.type == 'image':
		# 	image = Image.objects.get(id=value)
		# 	if image:
		# 		preview = "<img src='{src}' style='max-width:200px;max-height:200px;' />".format(src=image.url)
		elif self.type == 'url':
			preview = "<a href='{url}'>{url}</a>".format(url=value)
		elif self.type == 'email':
			preview = "<a href='mailto:{email}'>{email}</a>".format(email=value)
		elif self.type == 'phone':
			preview = "<a href='tel:{unformatted}'>{formatted}</a>".format(unformatted=slugify(value), formatted=value)
		elif self.type == 'html':
			preview = escape(value[:255] + (" ... " if len(value) > 255 else ""))
		elif self.type in ['javascript', 'css']:
			pass
		else:
			preview = value
		return mark_safe(preview)
	preview.allow_tags = True

	def save(self, request=None, *args, **kwargs):

		if self.key:
			self.key = slugify(self.key).replace("-", "_")

		cache_key = Setting.context_cache_key(site=self.site)
		cache.delete(cache_key)
		context = Setting.context(site=self.site)
		cache.set(cache_key, json.dumps(context), None)

		super(Setting, self).save(*args, **kwargs)

		if self.original['value'] != self.value:
			version = Version.objects.create(
				setting = self,
				value = self.value,
			)

	def delete(self, request=None, *args, **kwargs):
		cache_key = Setting.context_cache_key(site=self.site)
		cache.delete(cache_key)
		super(Setting, self).delete(*args, **kwargs)


class Version(models.Model):

	def __unicode__(self):
		return str(self.setting.path())
	def __str__(self):
		return str(self.setting.path())

	class Meta:
		verbose_name = "Version"
		verbose_name_plural = "Versions"
		managed = True
		unique_together = (
			("setting", "created"),
		)
		ordering = ['-created']

	# objects = Manager()

	id = models.AutoField(primary_key=True, null=False, blank=False, editable=False, db_column='id')
	setting = models.ForeignKey(Setting, null=False, blank=False, editable=False, related_name="versions", on_delete=models.CASCADE)
	value = models.TextField(null=True, blank=True, editable=False)
	created = models.DateTimeField(null=True, blank=True, editable=False, auto_now_add=True)

	def get_absolute_url(self):
		if not self.pk:
			return ""
		return reverse("admin:config_version_change", kwargs={"object_id": self.id})

	def admin_link(self):
		if not self.pk:
			return ""
		return mark_safe("""<a href="{url}">Link</a>""".format(url=self.get_absolute_url()))

	def preview(self):
		if not self.pk:
			return ""
		if len(self.value) > 255:
			return ""
		return self.setting.preview(version=self)

	def revert_button(self):
		if not self.pk:
			return ""
		return mark_safe("""
			<a href="{url}" style="">Revert</a>
		""".format(url=reverse('config:revert', kwargs={"version_id": self.id})))
	revert_button.short_description = "Revert"

	def revert(self):
		if not self.pk:
			return None
		self.setting.value = self.value
		self.setting.save()

	def save(self, *args, **kwargs):
		super(Version, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		super(Version, self).delete(*args, **kwargs)
