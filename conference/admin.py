from django.contrib import admin
from conference.models import *
from django.contrib.sites.models import Site as DjangoSite


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
	fields = [
		'css', 'domain','folder',
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


# class ConferenceInline(admin.TabularInline):
# 	model = Conference
# 	raw_id_fields = []


# class PageInline(admin.TabularInline):
# 	model = Page
	# raw_id_fields = []


class ConferenceSessionSpeakersInlineAdmin(admin.TabularInline):
	model = ConferenceSession.speakers.through
	raw_id_fields = ['conferencesession']


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


class SpeakerAdmin(admin.ModelAdmin):
	search_fields = ['first_name', 'last_name']
	fields = ['first_name', 'last_name', 'description', 'img', 'is_keynote', 'keynote_type', 'slug']
	inlines = [
		ConferenceSessionSpeakersInlineAdmin,
	]
	list_filter = ['is_keynote', 'keynote_type']


class PageAdmin(admin.ModelAdmin):
	fields = ['title', 'text', 'conference', 'parent', 'excerpt', 'img', 'slug']
	inlines = [
		# PageInline,
	]
	raw_id_fields = ['img']


class AgentAdmin(admin.ModelAdmin):
	search_fields = ['first_name', 'last_name', 'company']
	fields = ['first_name', 'last_name', 'company', 'description', 'img', 'topic']
	inlines = [
		# ConferenceInline,
	]
	list_filter = ['conference_agents', 'topic']


class ConferenceSessionAdmin(admin.ModelAdmin):
	search_fields = ['title']
	list_filter = ['conference', 'visibility', 'topics', 'is_featured', 'difficulty_level']
	inlines = [
		ConferenceSessionTopicsInline,
	]


class ConferenceContactAdmin(admin.ModelAdmin):
	search_fields = ['name', 'email']
	list_filter = ['conference', ]


class FAQAdmin(admin.ModelAdmin):
	search_fields = ['question']
	list_filter = ['conference', ]


class SponsorAdmin(admin.ModelAdmin):
	search_fields = ['name', 'website']
	list_filter = ['conference_sponsors', ]


class ExhibitorAdmin(admin.ModelAdmin):
	search_fields = ['name', 'website']
	list_filter = ['conference_exhibitor', ]


class MenuItemAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_filter = ['site', 'is_header', 'is_footer']


class SessionScheduleAdmin(admin.ModelAdmin):
	search_fields = ['session']
	list_filter = ['topic']


admin.site.register(SessionTopic)
# admin.site.register(Img)
admin.site.register(ConferenceSession, ConferenceSessionAdmin)
admin.site.register(SessionSchedule, SessionScheduleAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Exhibitor, ExhibitorAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ConferenceContact, ConferenceContactAdmin)
admin.site.register(Page, PageAdmin)
admin.site.unregister(DjangoSite)
admin.site.register(PitchSlam)
admin.site.register(RegistrationOption)
admin.site.register(RegistrationTimeFrame)
admin.site.register(Conference, ConferenceAdmin)
