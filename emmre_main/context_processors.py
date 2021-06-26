from datetime import datetime, date


def what_site(request):
	requested_site = str(request.site)

	if 'emmre' in requested_site:
		webpage = request.site
	else:
		webpage = 'emmre'
	return webpage


# def emmre_page_info(request):
# 	now = datetime.now()
# 	request.emmre = Conference.objects.filter(site=request.site, is_active=True, end_date__gte=now).order_by(
# 		'-start_date').first()
# 	return request.emmre


def ContextProcessor(request):

	# menu_items = MenuItem.objects.filter(parent__isnull=True, site=request.site)
	# conference_name = conference_page_info(request)
	webpage = what_site(request)

	return {
		# "menu_items": menu_items,
		'site': webpage,
		# 'emmre_main': conference_name,
	}