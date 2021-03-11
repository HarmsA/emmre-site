from django.db import models
from django.contrib.sites.models import Site as DjangoSite
from django.utils.text import slugify
import os
from writersdigest.settings import BASE_DIR
from media.models import Image
from conference.managers import Manager


class Site(models.Model):
	objects = Manager()
	folders = os.listdir(str(BASE_DIR).rstrip('/')+"/conference/static/")
	slug_choices=[]
	for folder in folders:
		slug_choices.append((folder,folder))
	css = models.TextField(blank=True, null=True)
	domain = models.CharField(max_length=200, blank=False, null=False)
	folder = models.SlugField(max_length=255, choices=slug_choices, verbose_name='Folder', null=True, blank=True, unique=True)

	def __str__(self):
		return self.domain


class SessionTopic(models.Model):
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


# class Img(models.Model):
# 	img_url = models.URLField(blank=True, null=True)
# 	alt = models.CharField(max_length=50, null=True, blank=True)
#
# 	def __str__(self):
# 		return self.alt


class ConferenceSession(models.Model):
	published_status_choices = (
		('draft', 'Draft'),
		('published', 'Published'),
		('pending_review', 'Pending Review'),
	)
	difficulty_level_choices = (
		('beginner', 'Beginner'),
		('intermediate', 'Intermediate'),
		('pitch_slam_participants', 'Pitch Slam Participants'),
		('all_levels', 'All Levels'),
		('general', 'General'),
	)

	topics = models.ManyToManyField(SessionTopic, related_name='conference_sessions', through='SessionSchedule')
	title = models.CharField(max_length=500, blank=True, null=True)
	description = models.TextField()
	published_status = models.CharField(max_length=30, choices=published_status_choices)
	visibility = models.BooleanField(default=True)
	date_published = models.DateTimeField()
	difficulty_level = models.CharField(max_length=30, choices=difficulty_level_choices, blank=True)
	speakers = models.ManyToManyField('Speaker', related_name='conference_sessions', verbose_name='Speakers', blank=True)
	sponsors = models.ManyToManyField('Sponsor', related_name='conference_sessions', verbose_name='Sponsors', blank=True)
	conference = models.ForeignKey('Conference', related_name='conference_sessions', on_delete=models.CASCADE, null=True, blank=True)
	is_featured = models.BooleanField(default=False)
	slug = models.SlugField(max_length=100, blank=True, null=True)


	def save(self, *args, **kwargs):
		if self.title and not self.slug:
			self.slug = slugify(self.title)
		super(type(self), self).save(*args, **kwargs)

	def __str__(self):
		return self.title


class SessionSchedule(models.Model):
	class Meta:
		unique_together = ('session', 'topic', 'start', 'end')

	session = models.ForeignKey(ConferenceSession, related_name='session_schedules', on_delete=models.CASCADE)
	topic = models.ForeignKey(SessionTopic, related_name='session_schedules', on_delete=models.CASCADE)
	start = models.DateTimeField(blank=True, null=True)
	end = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return f"{self.session}, under {self.topic}"


class Speaker(models.Model):
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	img = models.ForeignKey(Image, related_name='speakers', on_delete=models.CASCADE, blank=True, null=True)
	is_keynote = models.BooleanField(default=False)
	keynote_type = models.CharField(max_length=100, blank=True, null=True, default='')
	slug = models.SlugField(max_length=100, blank=True, null=True)

	def save(self, *args, **kwargs):
		name = self.first_name + ' ' + self.last_name
		if name and not self.slug:
			self.slug = slugify(name)
		super(type(self), self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Agent(models.Model):
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	company = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	img = models.ForeignKey(Image, related_name='agents', on_delete=models.CASCADE, blank=True, null=True)
	topic = models.ManyToManyField(SessionTopic, related_name='agent_topics', blank=True)
	slug = models.SlugField(max_length=100, blank=True, null=True)

	class Meta:
		ordering = ('last_name',)

	def save(self, *args, **kwargs):
		name = self.first_name + ' ' + self.last_name
		if name and not self.slug:
			self.slug = slugify(name)
		super(type(self), self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Sponsor(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	website = models.URLField(max_length=255, blank=True, null=True)
	img = models.ForeignKey(Image, related_name='sponsors', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.name


class Exhibitor(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	website = models.URLField(max_length=255, blank=True, null=True)
	img = models.ForeignKey(Image, related_name='exhibitors', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.name


class Conference(models.Model):
	title = models.CharField(max_length=100, blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	start_date = models.DateField()
	end_date = models.DateField()
	sponsors = models.ManyToManyField(Sponsor, related_name='conference_sponsors', verbose_name='Sponsor',)
	exhibitor = models.ManyToManyField(Exhibitor, related_name='conference_exhibitor', verbose_name='Exhibitor',)
	agents = models.ManyToManyField(Agent, related_name='conference_agents', verbose_name='Agent')
	site = models.ForeignKey(Site, null=False, blank=False, related_name='conferences', on_delete=models.PROTECT)
	cancel_refund = models.TextField()
	basic_conference = models.TextField()
	all_access_conference = models.TextField()
	is_active = models.BooleanField(default=False)
	register_url = models.URLField(blank=True, null=True)

	def __str__(self):
		return self.title


class NavLink(models.Model):
	title = models.CharField(max_length=50)
	conference = models.ForeignKey(Conference, related_name='navlinks', on_delete=models.CASCADE)


class ConferenceAddOn(models.Model):
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=255, blank=True, null=True)
	date = models.DateField()
	conference = models.ForeignKey(Conference, related_name='conference_AddOns', on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class ConferenceContact(models.Model):
	name = models.CharField(max_length=25, blank=True, null=True)
	title = models.CharField(max_length=25, blank=True, null=True)
	contact_for = models.CharField(max_length=255, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	phone = models.PositiveBigIntegerField(blank=True, null=True)
	novel = models.BooleanField(default=True)
	annual = models.BooleanField(default=True)
	conference = models.ForeignKey(Conference, related_name='conference_contact', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.name} for {self.conference}'


class FAQ(models.Model):
	question = models.CharField(max_length=255, blank=True, null=True)
	answer = models.TextField(blank=True, null=True)
	conference = models.ForeignKey(Conference, related_name='conference_faq', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.conference} -- Question -- {self.question}'


class PitchSlam(models.Model):
	description = models.TextField(blank=True, null=True)
	conference = models.ForeignKey(Conference, related_name='conference_pitchslam', on_delete=models.CASCADE, blank=True, null=True)
	imgs = models.ManyToManyField(Image, related_name='pitchslam', blank=True)

	def __str__(self):
		return f'{self.conference} Pitch-Slam'


class RegistrationOption(models.Model):
	class Meta:
		unique_together = ('title', 'conference')

	title = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	conference = models.ForeignKey(Conference, related_name='conference_registration', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.title} -- {self.conference.title}'


class RegistrationTimeFrame(models.Model):
	class Meta:
		unique_together = ('registration', 'start', 'end')

	registration = models.ForeignKey(RegistrationOption, related_name='time_frames', on_delete=models.CASCADE, blank=True, null=True)
	cost = models.IntegerField(blank=True, null=True)
	start = models.DateField(blank=True, null=True)
	end = models.DateField(blank=True, null=True)

	def __str__(self):
		return f'{self.registration.title} -- {self.start} -- ${self.cost}'


# TODO  make menu items orderable by admin
class MenuItem(models.Model):
	class Meta:
		ordering = ['order', 'id']
	name = models.CharField(max_length=100, blank=True, null=True)
	parent = models.ForeignKey('self', related_name="children", blank=True, null=True, on_delete=models.CASCADE)
	link = models.CharField(max_length=100, blank=True, null=True)
	site = models.ForeignKey(Site, null=True, blank=True, related_name='site_menu_item', on_delete=models.PROTECT)
	is_header = models.BooleanField(default=True)
	is_footer = models.BooleanField(default=True)
	order = models.IntegerField(default=99)

	def __str__(self):
		return self.name


class Page(models.Model):
	class Meta:
		unique_together = (('conference', 'title'), ('conference', 'slug'))

	slug = models.SlugField(max_length=255, blank=True, null=False)
	text = models.TextField(blank=True, null=True)
	title = models.CharField(max_length=100, blank=False, null=False)
	conference = models.ForeignKey(Conference, related_name='pages', blank=False, null=False, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	img = models.ForeignKey(Image, related_name='pages', blank=True, null=True, on_delete=models.CASCADE)
	parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
	excerpt = models.TextField(blank=True, null=True, verbose_name='Intro for link')

	def save(self, *args, **kwargs):
		if self.title and not self.slug:
			self.slug = slugify(self.title)
		super(type(self), self).save(*args, **kwargs)

	def __str__(self):
		return self.title


