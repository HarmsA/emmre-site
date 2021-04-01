from django.http import Http404

from conference.forms import AccessibilitySettingsForm
from .models import *
from django.shortcuts import render
from django.views.decorators.http import require_safe
from datetime import datetime, date
from collections import OrderedDict
from pprint import pprint
from ordered_set import OrderedSet
from config.models import Setting as AdminSettings
from .context_processors import conference_page_info
from .context_processors import what_site



# def conference_page_info(request):
# 	now = datetime.now()
# 	request.conference = Conference.objects.filter(site=request.site, is_active=True, end_date__gte=now).order_by(
# 		'-start_date').first()
# 	# print(request.conference)
# 	requested_site = str(request.site)
#
# 	if 'novel' in requested_site:
# 		webpage = request.site
# 	else:
# 		webpage = 'annual'
# 	context = {
# 		'conference': webpage,
# 	}
# 	return webpage, request.conference


def home(request):
	conference = conference_page_info(request)
	conference_speakers = Speaker.objects.filter(conference_sessions__conference__title=conference).distinct()

	context = {
		'speakers': conference_speakers,
	}
	return render(request, 'conference/home.html', context=context)


def schedule(request):
	conference = conference_page_info(request)

	c_sessions = ConferenceSession.objects.filter(conference__site=request.site, is_featured=False)
								# .order_by('topics__start').prefetch_related('topics')

	featured_sessions = ConferenceSession.objects.filter(conference__site=request.site, is_featured=True) \
		# .order_by('topics__start').prefetch_related('topics')
	session_schedules = SessionSchedule.objects.filter(session__in=c_sessions).order_by('start')
	days = OrderedSet()
	for date in list(session_schedules.distinct().values_list('start', flat=True)):
		if not date:
			continue
		days.append(date.day)
	topics = SessionTopic.objects.filter(conference_sessions__in=c_sessions).distinct()

	times = OrderedSet()

	for session_schedule in session_schedules:
		if not session_schedule.start:
			continue
		times.add((session_schedule.start, session_schedule.end))
	table_data = OrderedDict()
	for day in days:
		table_data[day] = {}
		for topic in topics:
			table_data[day][topic.name] = OrderedDict()
			for time in times:
				if time[0].day != day:
					continue
				table_data[day][topic.name][time] = None

	for conference_session in c_sessions:
		for session_schedule in conference_session.session_schedules.all():
			if not session_schedule.start:
				continue
			table_data[session_schedule.start.date().day][session_schedule.topic.name][(session_schedule.start, session_schedule.end)] = conference_session

	cols_to_be_deleted = []
	for date, day in table_data.items():
		for topic_name, timeslots in day.items():
			delete_column = True
			for conference_session in timeslots.values():
				if conference_session:
					delete_column = False
					break
			if delete_column:
				cols_to_be_deleted.append((date,topic_name))

	for col in cols_to_be_deleted:
		del table_data[col[0]][col[1]]

	times = set(times)
	sessions = ConferenceSession.objects.filter(conference__title=conference).order_by('topics__name')

	speakers = Speaker.objects.filter()
	context = {
		'featured_sessions': featured_sessions,
		'topics': topics,
		'table_data': table_data,
		"speakers": speakers,
		'sessions': sessions,
	}
	return render(request, 'conference/schedule.html', context=context)


def speakers(request):
	conference = conference_page_info(request)
	conference_speakers = Speaker.objects.filter(conference_sessions__conference__title=conference).distinct().order_by('last_name')

	context = {
		'speakers': conference_speakers,
	}
	return render(request, 'conference/speakers.html', context=context)


def pitchslam(request):
	conference = conference_page_info(request)
	pitchslam = PitchSlam.objects.filter(conference__title=conference).distinct()
	register_url = Conference.objects.get(title=conference)
	img_file = []

	context = {
		'pitchslam': pitchslam,
		'img_file': img_file,
		'register_url': register_url,
	}
	return render(request, 'conference/pitch_slam.html', context=context)


def agents_editors(request):
	conference = conference_page_info(request)
	agents = Agent.objects.filter(conference_agents__title=conference).distinct()
	# conference = Conference.objects.get(title=conference)
	topic_list = SessionTopic.objects.all()

	context = {
		'agents': agents,
		'topic_list': topic_list,
	}
	return render(request, 'conference/agents.html', context=context)


def newsletter(request):
	conference = conference_page_info(request)
	context = {

	}
	return render(request, 'conference/newsletter.html', context=context)


def sponsors_exhibitors(request):
	conference = conference_page_info(request)
	sponsors = Sponsor.objects.filter(conference_sponsors__title=conference)
	exhibitors = Exhibitor.objects.filter(conference_exhibitor=conference)

	context = {
		'sponsors': sponsors,
		'exhibitors': exhibitors,

	}
	return render(request, 'conference/sponsor_and_exibitors.html', context=context)


def register(request):
	today = date.today()
	conference = conference_page_info(request)

	options = RegistrationTimeFrame.objects.filter(registration__conference__title=conference).order_by('start')
	details = RegistrationOption.objects.filter(conference__title=conference)
	register_url = Conference.objects.get(title=conference)

	add_ons = ConferenceAddOn.objects.filter(conference__title=conference)

	options_list = OrderedSet()
	for option in options:
		options_list.append(option.registration.title)

	dates = OrderedSet()
	registration_options = OrderedDict()
	for option_title in options_list:
		registration_options[option_title] = {}
		for option in options:
			if option.registration.title == option_title:
				registration_options[option_title][(option.start, option.end)] = {}
				registration_options[option_title][(option.start, option.end)]={option.cost}
	# pprint(registration_options)

	context = {
		'options': options,
		'registration_options': registration_options,
		'details': details,
		'register_url': register_url,
		'add_ons': add_ons,
		'today': today,
	}
	return render(request, 'conference/register.html', context=context)


def session(request, slug):
	conference = conference_page_info(request)
	session = ConferenceSession.objects.get(slug=slug)
	context = {
		'session': session,
	}
	return render(request, 'conference/session.html', context=context)


def speaker(request, slug):
	conference = conference_page_info(request)
	speakerobj = Speaker.objects.get(slug=slug)
	speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug).order_by('speakers__last_name')
	context = {
		'speaker': speakerobj,
		'speakers_conferences': speakers_conferences,
	}
	return render(request, 'conference/speaker.html', context=context)


def agent(request, slug):
	conference = conference_page_info(request)
	agent = Agent.objects.get(slug=slug)
	speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug)
	# print(agent)
	context = {
		'agent': agent,
		'speakers_conferences': speakers_conferences,

	}
	return render(request, 'conference/agent.html', context=context)


def faq(request):
	conference = conference_page_info(request)
	questions = FAQ.objects.filter(conference__title=conference)
	context = {
		'questions': questions,
	}
	return render(request, 'conference/faq.html', context=context)


def contact_us(request):
	conference = conference_page_info(request)
	contacts = ConferenceContact.objects.filter(conference__title=conference)
	context = {
		'contacts': contacts,
	}
	return render(request, 'conference/contact_us.html', context=context)


def page(request, slug):
	page = Page.objects.get(slug=slug)
	if not page:
		raise Http404()
	# raise Exception(page)
	context = {
		'page': page,

	}
	return render(request, 'conference/page.html', context=context)


def featured_events(request, slug):
	page = Page.objects.filter(conference=request.conference)
	page_obj = Page.objects.filter(slug=slug)

	context = {
		'page': page,
		'slug_page': page_obj,

	}
	return render(request, 'conference/featured_events.html', context=context)


@require_safe
def accessibility(request):
	accessibility_settings_form = AccessibilitySettingsForm()
	response = render(request, 'conference/accessibility.html', {
		"accessibility_settings_form": accessibility_settings_form,
	})
	return response



# def featured_event(request, slug):
# 	webpage, conference_name = conference_page_info(request)
# 	page = Page.objects.filter(conference=request.conference)
# 	page_obj = Page.objects.filter(slug=slug)
#
# 	context = {
# 		'site': webpage,
# 		'conference': request.conference,
# 		'page': page,
# 		'slug_page': page_obj,
#
# 	}
# 	return render(request, 'conference/featured_event.html', context=context)
#
