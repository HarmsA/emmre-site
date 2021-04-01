from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.views.generic import RedirectView

from media.views import *

app_name = "media"

urlpatterns = [
	path('image/<int:id>/thumbnail/', image_thumbnail, name='image_thumbnail'),
]