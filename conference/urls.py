from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    # path('novel_writers_digest_conference/', views.novel_writers_digest_conference, name='novel_writers_digest_conference'),
    # path('annual/', views.annual, name='annual'),
    path('schedule/', views.schedule, name='schedule'),
    path('speakers/', views.speakers, name='speakers'),
    path('pitch-slam/', views.pitchslam, name='pitch_slam'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('connect/', views.connect, name='connect'),
    path('sponsors-exhibitors/', views.sponsors_exhibitors, name='sponsors_exhibitors'),
    path('news/', views.news, name='news'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('faq/', views.faq, name='faq'),
    path('speaker/<slug:slug>/', views.speaker, name='speaker'),
    path('session/<slug:slug>/', views.session, name='session'),
    path('workshop/<slug:slug>/', views.featured_events, name='workshop'),
    path('workshop/<slug:slug>/', views.featured_event, name='workshop'),
    path('<slug:slug>/', views.page, name='page'),

# TODO add agent and agents path

]
