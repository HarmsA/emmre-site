from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('newsletter/', views.newsletter, name='newsletter'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/<slug:slug>/', views.blog, name='blog'),
    # path('news/', views.news, name='news'),
    # path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('product/', views.product, name='product'),
    # path('contact-us/', views.contact_us, name='contact_us'),
    path('faq/', views.faq, name='faq'),
    path('accessibility/', views.accessibility, name='accessibility'),
    # path('<slug:slug>/', views.page, name='page'),
]
