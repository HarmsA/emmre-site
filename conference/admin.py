from django.contrib import admin
from conference.models import *
from django.contrib.sites.models import Site as DjangoSite


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
	fields = [
		'css', 'domain', 'folder'
	]


class ConferenceSessionInline(admin.TabularInline):
	model = ConferenceSession
	# raw_id_fields = ['conference', 'speakers','ConferenceSession']


class ConferenceSponsorInline(admin.TabularInline):
	model = Conference.sponsors.through
	raw_id_fields = ['conference', 'sponsor']


class ExhibitorInline(admin.TabularInline):
	model = Conference.exhibitor.through
	raw_id_fields = ['conference', 'exhibitor']


class AgentInline(admin.TabularInline):
	model = Conference.agents.through
	# raw_id_fields = ['conference', 'agent']


class RegistrationOptionInline(admin.TabularInline):
	model = Conference.exhibitor.through
	raw_id_fields = ['conference', 'exhibitor']


class ConferenceSessionTopicsInline(admin.TabularInline):
	model = ConferenceSession.topics.through
	raw_id_fields = []


class ConferenceAddOnInline(admin.TabularInline):
	model = ConferenceAddOn
	raw_id_fields = []


class ConferenceContactInline(admin.TabularInline):
	model = ConferenceContact
	raw_id_fields = []


class ConferenceSessionSpeakersInlineAdmin(admin.TabularInline):
	model = ConferenceSession.speakers.through
	raw_id_fields = ['conferencesession']


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
	inlines = [
		ConferenceSessionInline, ConferenceSponsorInline,
		ExhibitorInline, ConferenceAddOnInline, ConferenceContactInline,
		AgentInline,
	]
	fields = [
		'title', 'site', 'register_url',
		'is_active', 'cancel_refund', 'basic_conference',
		'all_access_conference', 'location', 'start_date', 'end_date',
	]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
	search_fields = ['first_name', 'last_name']
	fields = ['first_name', 'last_name', 'description', 'img', 'is_keynote', 'keynote_type', 'slug']
	inlines = [
		ConferenceSessionSpeakersInlineAdmin,
	]
	list_filter = ['is_keynote', 'keynote_type']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
	fields = ['title', 'text', 'conference', 'parent', 'excerpt', 'img', 'slug']
	inlines = [
		# PageInline,
	]
	raw_id_fields = ['img']


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
	search_fields = ['first_name', 'last_name', 'company']
	fields = ['first_name', 'last_name', 'company', 'description', 'img', 'topic']
	inlines = [
		# ConferenceInline,
	]
	list_filter = ['conference_agents', 'topic']


@admin.register(ConferenceSession)
class ConferenceSessionAdmin(admin.ModelAdmin):
	search_fields = ['title']
	list_filter = ['conference', 'visibility', 'topics', 'is_featured', 'difficulty_level']
	inlines = [
		ConferenceSessionTopicsInline,
	]


@admin.register(ConferenceContact)
class ConferenceContactAdmin(admin.ModelAdmin):
	search_fields = ['name', 'email']
	list_filter = ['conference', ]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
	search_fields = ['question']
	list_filter = ['conference', ]


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
	search_fields = ['name', 'website']
	list_filter = ['conference_sponsors', ]


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
	search_fields = ['name', 'website']
	list_filter = ['conference_exhibitor', ]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_filter = ['site', 'is_header', 'is_footer']


@admin.register(SessionSchedule)
class SessionScheduleAdmin(admin.ModelAdmin):
	search_fields = ['session']
	list_filter = ['topic']


admin.site.register(SessionTopic)
admin.site.unregister(DjangoSite)
admin.site.register(PitchSlam)
admin.site.register(RegistrationOption)
admin.site.register(RegistrationTimeFrame)
