from conference.models import MenuItem

def ContextProcessor(request):

	menu_items = MenuItem.objects.filter(parent__isnull=True, site=request.site)

	return {
		"menu_items": menu_items,
	}