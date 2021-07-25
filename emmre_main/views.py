from django.http import Http404

from emmre_main.forms import AccessibilitySettingsForm
from .models import *
from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
from datetime import datetime, date
from collections import OrderedDict
from pprint import pprint
from ordered_set import OrderedSet
from config.models import Setting as AdminSettings
# from .context_processors import conference_page_info
from .context_processors import what_site
from .forms import BlogForm, CommentForm
from django.shortcuts import get_object_or_404


# def conference_page_info(request):
# 	now = datetime.now()
# 	request.emmre_main = Conference.objects.filter(site=request.site, is_active=True, end_date__gte=now).order_by(
# 		'-start_date').first()
# 	# print(request.emmre_main)
# 	requested_site = str(request.site)
#
# 	if 'novel' in requested_site:
# 		webpage = request.site
# 	else:
# 		webpage = 'annual'
# 	context = {
# 		'emmre_main': webpage,
# 	}
# 	return webpage, request.emmre_main

def home(request):

    context = {
        'title': 'Home',
    }
    return render(request, 'emmre_main/home.html', context=context)

def product(request):
    price_plans = PricePlan.objects.all()

    context = {
        'plans': price_plans,
    }
    return render(request, 'emmre_main/product.html', context=context)


def plans(request):
    price_plans = PricePlan.objects.all()

    context = {
        'plans': price_plans,
    }
    return render(request, 'emmre_main/product.html', context=context)


def blogs(request):
    blogs = Blog.objects.all().order_by('-date_published')
    p = Paginator(blogs, 2)
    print('Number of pages', p.num_pages)
    category_list = []
    category_list_items = []
    for blog in blogs:
        # print(category.name)
        # print(category_list)
        if blog.category.name not in category_list:
            # print(category.name)
            category_list.append(blog.category.name)
            category_list_items.append(blog)

    # for item in category_list_items:
    #     print(item)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {
        'title': 'Emmre Blogs',
        'blogs': page,
        'first_blog_category': category_list_items,
    }
    return render(request, 'emmre_main/blogs.html', context=context)


def blog(request, slug):
    if request.method == "POST":
        print(request.POST)
    comment_form = CommentForm()
    blogs = Blog.objects.filter(slug=slug)
    print(blogs)
    blog = Blog.objects.get(slug=slug)
    comments = Comment.objects.filter(comment__slug=slug)
    context = {
        'blog':blog,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request, 'emmre_main/blog.html', context=context)


def newsletter(request):
    context = {

    }
    return render(request, 'emmre_main/newsletter.html', context=context)


def about(request):
    context = {

    }
    return render(request, 'emmre_main/about.html', context=context)


def faq(request):
    questions = FAQ.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'emmre_main/faq.html', context=context)


def page(request, slug):
    page = Page.objects.get(slug=slug)
    if not page:
        raise Http404()
    # raise Exception(page)
    context = {
        'page': page,

    }
    return render(request, 'emmre_main/page.html', context=context)


def blogform(request):
    blogform = BlogForm()

    if request.method == "POST":
        form = BlogForm(request.POST)
        print(form)
    context = {
        'blogform': blogform
    }
    return render(request, 'emmre_main/blog-form.html', context=context)



@require_safe
def accessibility(request):
    accessibility_settings_form = AccessibilitySettingsForm()
    response = render(request, 'emmre_main/accessibility.html', {
        "accessibility_settings_form": accessibility_settings_form,
    })
    return response
