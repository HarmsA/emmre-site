import base64
import datetime
import os
import re
from io import BytesIO

from PIL import Image as PILImage
from django.contrib.sites.models import Site as DjangoSite
from django.core.files.base import ContentFile
from django.db import models
from django.utils.html import strip_tags
from django.utils.text import slugify

from emmre_main.managers import Manager
from media.models import Image
from emmre.settings import BASE_DIR


class Site(models.Model):
    objects = Manager()
    folders = os.listdir(str(BASE_DIR).rstrip('/') + "/assets/")
    slug_choices = []
    for folder in folders:
        slug_choices.append((folder, folder))
    css = models.TextField(blank=True, null=True)
    domain = models.CharField(max_length=200, blank=False, null=False)
    folder = models.SlugField(max_length=255, choices=slug_choices, verbose_name='Folder', null=True, blank=True,
                              unique=True)

    def __str__(self):
        return self.domain


class Tag(models.Model):
    name = models.CharField(max_length=75, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super(type(self), self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=75, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super(type(self), self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Blog(models.Model):
    published_status_choices = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('pending_review', 'Pending Review'),
    )

    tag = models.ManyToManyField(Tag, related_name='blog', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='blog', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    img = models.ForeignKey(Image, related_name='blog', on_delete=models.CASCADE, blank=True, null=True)
    published_status = models.CharField(max_length=30, choices=published_status_choices)
    visibility = models.BooleanField(default=True)
    date_published = models.DateField()

    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            stripped = strip_tags(self.title)
            remove_p = stripped[1:-1]
            self.slug = slugify(remove_p)
        super(type(self), self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.category} - {self.slug} -- {self.date_published}'


class Comment(models.Model):
    comment = models.ForeignKey(Blog, related_name='blog', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    author = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    parent_comment = models.ForeignKey('self', related_name='child_comment', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment dated: {self.date} -- Approved: {self.approved}'


class PricePlan(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    button = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=25, blank=True, null=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.title}, color {self.color}"


class FAQ(models.Model):
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    img = models.ForeignKey(Image, related_name='faq', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Question -- {self.question}'


class Page(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=False)
    text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    img = models.ForeignKey(Image, related_name='pages', blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    excerpt = models.TextField(blank=True, null=True, verbose_name='Intro for link')
    css = models.TextField(blank=True, null=True)

    @staticmethod
    def parsecontentforimages(text):
        if not text:
            return text
        matches = re.finditer(r'<img src="data:(.*?);base64,(.*?)".*?>', text)
        if not matches:
            return text

        filenum = 0
        for match in matches:
            mimetype = match.group(1).lower()
            extension = mimetype.split('/')[1]
            # Save the image in memory
            im = PILImage.open(BytesIO(base64.b64decode(match.group(2))))
            out_im2 = BytesIO()
            im.save(out_im2, extension)
            file_name = "base64image_" + str('page_img') + str(filenum) + ' ' + str(__class__.__name__) + str(
                id) + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + "." + str(extension)
            filenum += 1
            img = Image()
            img.file.save(file_name, ContentFile(out_im2.getvalue()))
            img.save()
            # raise Exception(match.group(0))
            text = text.replace(str(match.group(0)), f"""<img src="{img.url}"/>""")
        return text

    def save(self, *args, **kwargs):
        self.text = Page.parsecontentforimages(self.text)
        if self.title and not self.slug:
            self.slug = slugify(self.title)
        super(type(self), self).save(*args, **kwargs)

    def __str__(self):
        return self.title

