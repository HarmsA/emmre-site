from django.shortcuts import render
from .models import ConferenceSession, Img, Sponsor, Exhibitor, NavLink, ConferenceAddOn, ConferenceContact, \
					Conference, SessionTopic, Speaker, FAQ, SessionSchedule, PitchSlam, RegistrationOption, \
					RegistrationTimeFrame, Page
from datetime import datetime
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


# def novel_writers_digest_conference(request):
# 	context = {
# 		'conference': 'novel_writers_digest_conference',
# 	}
# 	return render(request, 'conference/home.html', context=context)


# def annual(request):
# 	context = {
# 		'conference': 'annual',
# 	}
# 	return render(request, 'conference/home.html', context=context)


def schedule(request):
	webpage, conference = conference_page_info(request)
	# print('8'*89, webpage, request.site)
	# conference = Conference.objects.filter(id=request.site.id)
	c_sessions = ConferenceSession.objects.filter(conference__site=request.site, is_featured=False)
								# .order_by('topics__start').prefetch_related('topics')
	# print(c_sessions)
	# for c in c_sessions:
	# 	print(c.conference.site)
	featured_sessions = ConferenceSession.objects.filter(conference__site=request.site, is_featured=True) \
		# .order_by('topics__start').prefetch_related('topics')
	session_schedules = SessionSchedule.objects.filter(session__in=c_sessions).order_by('start')
	days = OrderedSet()
	for date in list(session_schedules.distinct().values_list('start', flat=True)):
		if not date:
			continue
		days.append(date.day)
	topics = SessionTopic.objects.filter(conferencesessions__in=c_sessions).distinct()

	# topic_set = []
	# for topic in topics:
	# 	topic_set.append(topic.name)
	# topic_set = set(topic_set)
	# session_dict = OrderedDict()
	times = OrderedSet()
	# for session in c_sessions:
	# 	# 	items = []
	# 	# 	times.append(session.start_date_time)
	# 	# 	for item in session.topics.all():
	# 	# 		items.append(item.name)
	# 	# 	speakers = []
	# 	# 	for speaker in session.related_speaker.all():
	# 	# 		speakers.append(speaker.name)
	# 	# 	session_dict[session.id] = {'title': session.title,
	# 	# 	                            'start_time': str(session.start_date_time),
	# 	# 	                            'topic': items,
	# 	# 	                            'speaker':speakers,
	# 	# 	                            }

	for session_schedule in session_schedules:
		if not session_schedule.start:
			continue
		times.add((session_schedule.start, session_schedule.end))
	# raise Exception(times)
	table_data = OrderedDict()
	for day in days:
		table_data[day] = {}
		for topic in topics:
			table_data[day][topic.name] = OrderedDict()
			for time in times:
				if time[0].day != day:
					continue
				# raise Exception(time)
				table_data[day][topic.name][time] = None
			# table_data

	# raise Exception(c_sessions)
	for conference_session in c_sessions:
		for session_schedule in conference_session.session_schedules.all():
			if not session_schedule.start:
				continue
			table_data[session_schedule.start.date().day][session_schedule.topic.name][(session_schedule.start, session_schedule.end)] = conference_session

	cols_to_be_deleted = []
	for date, day in table_data.items():
		# raise Exception(day)
		# print(day)
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
	# print(sessions[0].conference.start_date)
	# print(session_schedules[0].session.title)
	speakers = Speaker.objects.filter()
	print(speakers)
	context = {
		'site': webpage,
		'conference': conference,
		'sessions': c_sessions,
		'featured_sessions': featured_sessions,
		'topics': topics,
		'table_data': table_data,
		"speakers":speakers,
		'sessions': sessions,
	}
	return render(request, 'conference/schedule.html', context=context)


def speakers(request):
	webpage, conference = conference_page_info(request)
	conference_speakers = Speaker.objects.filter(conference_sessions__conference__title=conference).distinct().order_by('last_name')
	print(request.site)
	context = {
		'site': webpage,
		'conference': conference,
		'speakers': conference_speakers,
	}
	return render(request, 'conference/speakers.html', context=context)


def pitchslam(request):
	webpage, conference = conference_page_info(request)
	pitchslam = PitchSlam.objects.filter(conference__title=conference).distinct()
	img_url=[]
	print(webpage)

	for pics in pitchslam:
		print(pics.imgs)
		for pic in pics.imgs.all():
			if pic.img_url not in img_url:
				img_url.append(pic.img_url)
	print(img_url)
	context = {
		'site': webpage,
		'conference': request.conference,
		'pitchslam': pitchslam,
		'img_url': img_url,
	}
	return render(request, 'conference/pitch_slam.html', context=context)


def newsletter(request):
	webpage, conference = conference_page_info(request)
	context = {
		'site': webpage,
		'conference': request.conference,

	}
	return render(request, 'conference/newsletter.html', context=context)


def connect(request):
	webpage, conference = conference_page_info(request)

	context = {
		'site': webpage,
		'conference': request.conference,

	}
	return render(request, 'conference/connect.html', context=context)


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


def news(request):
	webpage, conference = conference_page_info(request)

	context = {
		'site': webpage,
		'conference': request.conference,

	}
	return render(request, 'conference/news.html', context=context)


def travel(request):
	webpage, conference = conference_page_info(request)

	context = {
		'site': webpage,
		'conference': request.conference,

	}
	return render(request, 'conference/page.html', context=context)


def register(request):
	webpage, conference_name = conference_page_info(request)
	# site = Conference.objects.filter(is_active=True)
	# registration_options = RegistrationOption.objects.filter(conference__title=conference_name)
	options = RegistrationTimeFrame.objects.filter(registration__conference__title=conference_name).order_by('registration')
	details = RegistrationOption.objects.filter(conference__title=conference_name)
	register_url = Conference.objects.filter(title=conference_name)
	add_ons = ConferenceAddOn.objects.filter(conference__title=conference_name)
	for add_on in add_ons:
		print(add_on)

	# for desc in details:
	# 	print(desc.description)
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
	}
	return render(request, 'conference/register.html', context=context)


def session(request, slug):
	webpage, conference = conference_page_info(request)
	session = ConferenceSession.objects.get(slug=slug)
	# speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug)
	print('*'*80, session.conference)
	context = {
		'site': webpage,
		'conference': request.conference,
		'session': session,
		# 'speakers_conferences': speakers_conferences,

	}
	return render(request, 'conference/session.html', context=context)


def speaker(request, slug):
	webpage, conference = conference_page_info(request)
	speakerobj = Speaker.objects.get(slug=slug)
	speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug).order_by('speakers__last_name')
	print(webpage)
	context = {
		'site': webpage,
		'conference': request.conference,
		'speaker': speakerobj,
		'speakers_conferences': speakers_conferences,

	}
	return render(request, 'conference/speaker.html', context=context)


def agent(request, slug):
	webpage, conference = conference_page_info(request)
	speakerobj = Speaker.objects.get(slug=slug)
	speakers_conferences = ConferenceSession.objects.filter(speakers__slug=slug)

	context = {
		'site': webpage,
		'conference': request.conference,
		'speaker': speakerobj,
		'speakers_conferences': speakers_conferences,

	}
	return render(request, 'conference/speaker.html', context=context)


def about(request):
	webpage, conference = conference_page_info(request)

	context = {
		'site': webpage,
		'conference': request.conference,

	}
	return render(request, 'conference/about.html', context=context)


def faq(request):
	webpage, conference = conference_page_info(request)
	questions = FAQ.objects.filter(conference__title=conference)
	print(questions)
	context = {
		'site': webpage,
		'conference': request.conference,
		'questions': questions,
	}
	return render(request, 'conference/faq.html', context=context)


def contact_us(request):
	# print('8'*80)
	webpage, conference = conference_page_info(request)
	contacts = ConferenceContact.objects.filter(conference__title=conference)
	print(contacts)
	context = {
		'site': webpage,
		'conference': request.conference,
		'contacts': contacts,

	}
	return render(request, 'conference/contact_us.html', context=context)


def page(request, slug):
	webpage, conference_name = conference_page_info(request)
	page = Page.objects.filter(conference=request.conference)
	print(slug)
	context = {
		'site': webpage,
		'conference': request.conference,
		'page': page,

	}
	return render(request, 'conference/page.html', context=context)

