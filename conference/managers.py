from django.db import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class Manager(models.Manager):

	def get(self, *args, **kwargs):
		try:
			result = super(Manager, self).get(*args, **kwargs)
		except ObjectDoesNotExist:
			result = None
		except MultipleObjectsReturned:
			result = super(Manager, self).filter(*args, **kwargs).first()
		except TypeError:
			result = None
		return result

	def get_object_or_404(self, *args, **kwargs):
		obj = self.get(*args, **kwargs)
		if obj:
			return obj
		else:
			raise Http404()

	def update_or_create(self, defaults={}, *args, **kwargs):
		created = False
		instance = self.get(*args, **kwargs)
		if not instance:
			instance = self.create(*args, **kwargs)
			created = True
		if defaults:
			for key, value in defaults.items():
				setattr(instance, key, value)
			instance.save(force_insert=False, force_update=True)
		return (instance, created)

	def get_or_create(self, defaults={}, *args, **kwargs):
		created = False
		instance = self.get(*args, **kwargs)
		if not instance:
			instance = self.create(*args, **kwargs)
			created = True
			if defaults:
				for key, value in defaults.items():
					setattr(instance, key, value)
				instance.save(force_insert=False, force_update=True)
		return (instance, created)

	def random(self, *args, **kwargs):
		instances = self.none()
		try:
			instances = self.filter(*args, **kwargs).order_by('?')
		except:
			pass
		return instances.first()
