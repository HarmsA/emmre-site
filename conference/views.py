from django.shortcuts import render
from .models import ConferenceSession, Sponsor, Exhibitor, NavLink, ConferenceAddOn, ConferenceContact, \
					Conference, SessionTopic, Speaker, FAQ, SessionSchedule, PitchSlam, RegistrationOption, \
					RegistrationTimeFrame, Page, MenuItem, Agent
from datetime import datetime, date
from collections import OrderedDict
from pprint import pprint
from ordered_set import OrderedSet


def conference_page_info(request):
	now = datetime.now()
	request.conference = Conference.objects.filter(site=request.site, is_active=True, end_date__gte=now).order_by(
		'-start_date').first()
	print(request.conference)
	requested_site = str(request.site)

	if 'novel' in requested_site:
		webpage = request.site
	else:
		webpage = 'annual'
	context = {
		'conference': webpage,
	}
	return webpage, request.conference


def home(request):
	webpage, conference = conference_page_info(request)
	conference_speakers = Speaker.objects.filter(conference_sessions__conference__title=conference).distinct()


	context = {
		'site': webpage,
		'conference': conference,
		'speakers': conference_speakers,
	}
	return render(request, 'conference/home.html', context=context)


def schedule(request):
	webpage, conference = conference_page_info(request)

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
	requested_site = str(request.site)
	sessions = ConferenceSession.objects.filter(conference__title=request.conference).order_by('topics__name')

	speakers = Speaker.objects.filter()
	context = {
		'site': webpage,
		'conference': conference,
		'featured_sessions': featured_sessions,
		'topics': topics,
		'table_data': table_data,
		"speakers": speakers,
		'sessions': sessions,
	}
	return render(request, 'conference/schedule.html', context=context)


def speakers(request):
	webpage, conference = conference_page_info(request)
	conference_speakers = Speaker.objects.filter(conference_sessions__conference__title=conference).distinct().order_by('last_name')

	context = {
		'site': webpage,
		'conference': conference,
		'speakers': conference_speakers,
	}
	return render(request, 'conference/speakers.html', context=context)


def pitchslam(request):
	webpage, conference = conference_page_info(request)
	pitchslam = PitchSlam.objects.filter(conference__title=conference).distinct()
	register_url = Conference.objects.get(title=conference)
	img_file = []

	context = {
		'site': webpage,
		'conference': request.conference,
		'pitchslam': pitchslam,
		'img_file': img_file,
		'register_url': register_url,
	}
	return render(request, 'conference/pitch_slam.html', context=context)


def agents_editors(request):
	webpage, conference = conference_page_info(request)
	agents = Agent.objects.filter(conference_agents__title=conference).distinct()
	# conference = Conference.objects.get(title=conference)
	topic_list = SessionTopic.objects.all()

	context = {
		'site': webpage,
		'conference': request.conference,
		'agents': agents,
		'topic_list': topic_list,
	}
	return render(request, 'conference/agents.html', context=context)


def newsletter(request):
	webpage, conference = conference_page_info(request)
	context = {
		'site': webpage,
		'conference': request.conference,

	}
	return render(request, 'conference/newsletter.html', context=context)


def sponsors_exhibitors(request):
	webpage, conference_name = conference_page_info(request)
	sponsors = Sponsor.objects.filter(conference_sponsors__title=conference_name)
	exhibitors = Exhibitor.objects.filter(conference_exhibitor=conference_name)

	context = {
		'site': webpage,
		'conference': request.conference,
		'sponsors': sponsors,
		'exhibitors': exhibitors,

	}
	return render(request, 'conference/sponsor_&_exibitors.html', context=context)


def register(request):
	today = date.today()
	webpage, conference_name = conference_page_info(request)

	options = RegistrationTimeFrame.objects.filter(registration__conference__title=conference_name).order_by('registration')
	details = RegistrationOption.objects.filter(conference__title=conference_name)
	register_url = Conference.objects.filter(title=conference_name)
	add_ons = ConferenceAddOn.objects.filter(conference__title=conference_name)

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
	pprint(registration_options)

	context = {
		'site': webpage,
		'conference': request.conference,
		'options': options,
		'registration_options': registration_options,
		'details': details,
		'register_url': register_url,
		'add_ons': add_ons,
		'today': today,
	}
	return render(request, 'conference/register.html', context=context)


def session(request, slug):
	webpage, conference = conference_page_info(request)
	session = ConferenceSession.objects.get(slug=slug)
	context = {
		'site': webpage,
		'conference': request.conference,
		'session': session,
	}
	return render(request, 'conference/session.html', context=context)


def speaker(request, slug):
	webpage, conference = conference_page_info(request)
	speakerobj = Speaker.objects.get(slug=slug)
	speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug).order_by('speakers__last_name')
	context = {
		'site': webpage,
		'conference': request.conference,
		'speaker': speakerobj,
		'speakers_conferences': speakers_conferences,

	}
	return render(request, 'conference/speaker.html', context=context)


def agent(request, slug):
	webpage, conference = conference_page_info(request)
	agent = Agent.objects.get(slug=slug)
	speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug)
	print(agent)
	context = {
		'site': webpage,
		'conference': request.conference,
		'agent': agent,
		'speakers_conferences': speakers_conferences,

	}
	return render(request, 'conference/agent.html', context=context)


def faq(request):
	webpage, conference = conference_page_info(request)
	questions = FAQ.objects.filter(conference__title=conference)
	context = {
		'site': webpage,
		'conference': request.conference,
		'questions': questions,
	}
	return render(request, 'conference/faq.html', context=context)


def contact_us(request):
	webpage, conference = conference_page_info(request)
	contacts = ConferenceContact.objects.filter(conference__title=conference)
	context = {
		'site': webpage,
		'conference': request.conference,
		'contacts': contacts,
	}
	return render(request, 'conference/contact_us.html', context=context)


def page(request, slug):
	webpage, conference_name = conference_page_info(request)
	page = Page.objects.filter(parent__conference=request.conference)
	page_obj = Page.objects.filter(slug=slug)

	context = {
		'site': webpage,
		'conference': request.conference,
		'page': page,
		'slug_page': page_obj,
		'slug': slug,

	}
	return render(request, 'conference/page.html', context=context)


def featured_events(request, slug):
	webpage, conference_name = conference_page_info(request)
	page = Page.objects.filter(conference=request.conference)
	page_obj = Page.objects.filter(slug=slug)

	context = {
		'site': webpage,
		'conference': request.conference,
		'page': page,
		'slug_page': page_obj,

	}
	return render(request, 'conference/featured_events.html', context=context)


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
