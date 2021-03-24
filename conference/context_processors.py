from conference.models import MenuItem
from datetime import datetime, date
from .models import Conference


def what_site(request):
	requested_site = str(request.site)

	if 'novel' in requested_site:
		webpage = request.site
	else:
		webpage = 'annual'
	return webpage


def conference_page_info(request):
	now = datetime.now()
	request.conference = Conference.objects.filter(site=request.site, is_active=True, end_date__gte=now).order_by(
		'-start_date').first()
	return request.conference


def ContextProcessor(request):

	menu_items = MenuItem.objects.filter(parent__isnull=True, site=request.site)
	conference_name = conference_page_info(request)
	webpage = what_site(request)

	return {
		"menu_items": menu_items,
		'site': webpage,
		'conference': conference_name,
	}