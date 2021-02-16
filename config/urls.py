from django.urls import path

from config.views import *

app_name = 'config'

urlpatterns = [
    path('revert/<int:version_id>/', revert, name='revert'),
]
