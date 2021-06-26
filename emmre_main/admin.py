from django.contrib import admin
from emmre_main.models import *
from django.contrib.sites.models import Site as DjangoSite


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
	fields = [
		'css', 'domain', 'folder'
	]


class CommentInline(admin.TabularInline):
	model = Comment
	# raw_id_fields = ['emmre_main', 'speakers']


# class Tagnline(admin.TabularInline):
# 	model = Tag
# 	# raw_id_fields = ['emmre_main', 'speakers']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	inlines = [
		CommentInline,
		# Tagnline,
	]



@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
	fields = ['title', 'parent', 'excerpt', 'img', 'slug', 'text', 'css']
	inlines = [
		# PageInline,
	]
	list_filter = ['title', ]
	raw_id_fields = ['img']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
	search_fields = ['question']
	# list_filter = ['emmre_main', ]


@admin.register(PricePlan)
class PricePlanAdmin(admin.ModelAdmin):
	search_fields = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']


admin.site.unregister(DjangoSite)
admin.site.register(Comment)
admin.site.register(Category)
