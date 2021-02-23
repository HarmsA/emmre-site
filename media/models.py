from django.db import models
from media.storage import s3_storage
from django.utils.text import slugify
from django.utils.safestring import mark_safe

status_codes = (
	(100, 'Continue'),
	(101, 'Switching Protocols'),
	(200, 'OK'),
	(202, 'Accepted'),
	(203, 'Non_Authoritative Information'),
	(204, 'No Content'),
	(205, 'Reset Content'),
	(206, 'Partial Content'),
	(300, 'Multiple Choices'),
	(301, 'Moved Permanently'),
	(302, 'Found'),
	(303, 'See Other'),
	(304, 'Not Modified'),
	(305, 'Use Proxy'),
	(306, 'Unused'),
	(307, 'Temporary Redirect'),
	(400, 'Bad Request'),
	(401, 'Unauthorized'),
	(402, 'Payment Required'),
	(403, 'Forbidden'),
	(404, 'Not Found'),
	(405, 'Method Not Allowed'),
	(406, 'Not Acceptable'),
	(407, 'Proxy Authentication Required'),
	(408, 'Request Timeout'),
	(409, 'Conflict'),
	(410, 'Gone'),
	(411, 'Length Required'),
	(412, 'Precondition Failed'),
	(413, 'Request Entity Too Large'),
	(414, 'Request URI Too Long'),
	(415, 'Unsupported Media Type'),
	(416, 'Request Range Not Satisfiable'),
	(417, 'Expectation Failed'),
	(500, 'Internal Server Error'),
	(501, 'Not Implemented'),
	(502, 'Bad Gateway'),
	(503, 'Service Unavailable'),
	(504, 'Gateway Timeout'),
	(505, 'HTTP Version Not Supported'),
)

def directory_path(instance, filename):
	model = slugify(instance.__class__._meta.verbose_name_plural)
	directory_path = "{model}/{filename}".format(
		model=model,
		filename=filename
	)
	return directory_path


class Media(models.Model):

	def __str__(self):
		return str(self.url)

	class Meta:
		verbose_name = "Media"
		verbose_name_plural = "Media"
		managed = True
		abstract = True
		ordering = ['-id']

	id = models.AutoField(primary_key=True, null=False, blank=False, editable=False, db_column='id')
	file = models.FileField(null=True, blank=True, storage=s3_storage, upload_to=directory_path)
	url = models.URLField(max_length=255, null=True, blank=True)
	type = models.CharField(max_length=255, null=True, blank=True)
	added = models.DateTimeField(null=True, blank=True, editable=False, auto_now_add=True)
	modified = models.DateTimeField(null=True, blank=True, editable=False, auto_now=True)

	def get_absolute_url(self):
		return self.url

	def save(self, request=None, *args, **kwargs):
		if not self.pk:
			super(Media, self).save(*args, **kwargs)
		if self.file:
			self.url = self.file.url
		super(Media, self).save(*args, **kwargs)

	def delete(self, request=None, *args, **kwargs):
		try:
			self.file.delete()
		except:
			pass
		super(Media, self).delete(*args, **kwargs)


class Image(Media):

	def __str__(self):
		return str(self.thumb())

	class Meta:
		verbose_name = "Image"
		verbose_name_plural = "Images"
		managed = True
		ordering = ['-id']

	color_spaces = (
		('1', '1'),
		('L', 'L'),
		('P', 'P'),
		('RGB', 'RGB'),
		('RGBA', 'RGBA'),
		('CYMK', 'CYMK'),
		('YCbCr', 'YCbCr'),
		('LAB', 'LAB'),
		('HSV', 'HSV'),
		('I', 'I'),
		('F', 'F'),
	)

	id = models.AutoField(primary_key=True, null=False, blank=False, editable=False, db_column='id')
	file = models.ImageField(null=True, blank=True, storage=s3_storage, upload_to=directory_path)
	alt = models.CharField(max_length=50, null=True, blank=True, default='Blank')

	def get_absolute_url(self):
		return self.url

	def thumb(self):
		if not self.pk:
			return ""
		return mark_safe("<img src='{src}' style='max-width:200px;max-height:200px;' />".format(src=self.url))
	thumb.allow_tags = True

	def preview(self):
		if not self.pk:
			return ""
		return mark_safe("<img src='{src}' />".format(src=self.url))
	preview.allow_tags = True

	def save(self, request=None, *args, **kwargs):
		if not self.pk:
			super(Image, self).save(*args, **kwargs)
		super(Image, self).save(*args, **kwargs)

	def delete(self, request=None, *args, **kwargs):
		try:
			self.file.delete()
		except:
			pass
		super(Image, self).delete(*args, **kwargs)


class PDF(Media):

	def __str__(self):
		return str(self.url)

	class Meta:
		verbose_name = "PDF"
		verbose_name_plural = "PDFs"
		managed = True
		ordering = ['-id']

	id = models.AutoField(primary_key=True, null=False, blank=False, editable=False, db_column='id')

	def get_absolute_url(self):
		return self.url

	def save(self, request=None, *args, **kwargs):
		self.type = "application/pdf"
		super(PDF, self).save(*args, **kwargs)

	def delete(self, request=None, *args, **kwargs):
		try:
			self.file.delete()
		except:
			pass
		super(PDF, self).delete(*args, **kwargs)
