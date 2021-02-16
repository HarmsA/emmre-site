from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from config.models import Version

@never_cache
@staff_member_required
@login_required
@require_GET
def revert(request, version_id):

    version = Version.objects.get(id=version_id)

    if not version:
    	raise Http404()

    version.revert()

    url = reverse("admin:config_setting_change", kwargs={"object_id": version.setting.id})

    response = HttpResponseRedirect(url)

    return response