from django.contrib import admin
from conference.models import SessionTopic, Img, ConferenceSession, \
	Speaker, Sponsor, Exhibitor, Conference, SessionSchedule, PitchSlam, FAQ, \
	RegistrationTimeFrame, RegistrationOption, Page, Site, Agent, ConferenceContact, \
	ConferenceAddOn


class SiteAdmin(admin.ModelAdmin):
	fields = [
		'css', 'domain','slug',
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


# class PageInline(admin.TabularInline):
# 	model = Page
	# raw_id_fields = []


class ConferenceSessionSpeakersInlineAdmin(admin.TabularInline):
	model = ConferenceSession.speakers.through
	raw_id_fields = ['conferencesession']


class ConferenceAdmin(admin.ModelAdmin):
	inlines = [
		ConferenceSessionInline, ConferenceSponsorInline,  ExhibitorInline, ConferenceAddOnInline, ConferenceContactInline
	]
	fields = [
		'title', 'site', 'register_url',
		'is_active', 'cancel_refund', 'basic_conference',
		'all_access_conference', 'location', 'start_date', 'end_date',
	]


class SpeakerAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'description', 'img', 'is_keynote', 'slug']
	inlines = [
		ConferenceSessionSpeakersInlineAdmin,
	]
	raw_id_fields = ['img']


class PageAdmin(admin.ModelAdmin):
	fields = ['title', 'text', 'conference', 'parent', 'child_intro']
	inlines = [
		# PageInline,
	]
	# raw_id_fields = ['img']


class AgentAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'company', 'description', 'img', 'topic']
	inlines = [
		# PageInline,
	]
	# raw_id_fields = ['img']


class ConferenceSessionAdmin(admin.ModelAdmin):
	search_fields = ['visibility']
	list_filter = ['conference', 'visibility', 'topics', 'is_featured', 'difficulty_level']
	inlines = [
		ConferenceSessionTopicsInline,
	]


admin.site.register(SessionTopic)
admin.site.register(Img)
admin.site.register(ConferenceSession, ConferenceSessionAdmin)
admin.site.register(SessionSchedule)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Sponsor)
admin.site.register(Exhibitor)
admin.site.register(FAQ)
admin.site.register(ConferenceContact)
admin.site.register(Page, PageAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(PitchSlam)
admin.site.register(RegistrationOption)
admin.site.register(RegistrationTimeFrame)
admin.site.register(Conference, ConferenceAdmin)

