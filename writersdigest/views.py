from django.views.decorators.http import require_safe
from .forms import AccessibilitySettingsForm
from django.shortcuts import render


@require_safe
def accessibility(request):
	accessibility_settings_form = AccessibilitySettingsForm()
	response = render(request, 'accessibility.html', {
		"accessibility_settings_form": accessibility_settings_form,
	})
	return response

