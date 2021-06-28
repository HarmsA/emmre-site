"""emmre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from emmre.settings import DEBUG
import emmre.views as views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emmre_main.urls')),
    path('config/', include('config.urls', namespace='config')),
    path('media/', include('media.urls', namespace='media')),
    path('accessibility/', views.accessibility, name="accessibility"),
    path('tinymce/', include('tinymce.urls')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns