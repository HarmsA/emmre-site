from django.contrib import admin
from media.models import *
from django.contrib import messages


def delete_queryset_with_file(self, request, queryset):
	for instance in queryset:
		if hasattr(instance, 'file'):
			try:
				instance.file.delete()
			except:
				pass
		instance.delete()
	messages.add_message(request, messages.SUCCESS, "Successfully deleted {count} {model}".format(count=queryset.count(), model=queryset.model.__name__))


delete_queryset_with_file.short_description = 'Delete selected'


def save_selected(modeladmin, request, queryset):
	for instance in queryset:
		instance.save()


save_selected.short_description = "Save selected"


class MediaAdmin(admin.ModelAdmin):
	list_filter = ['type', 'added', 'modified']
	list_display = ['id', 'file', 'url', 'type', 'added', 'modified']
	search_fields = ['id', 'file']
	list_editable = []
	list_display_links = ['id']
	ordering = ['-id']
	readonly_fields = ['id', 'added', 'modified']
	actions = [delete_queryset_with_file]
	list_per_page = 30
	raw_id_fields = []
	inlines = []
	fieldsets = (
		(None, {
			'fields': ('id', 'file', 'url', 'type', 'added', 'modified')
		}),
	)
	save_on_top = True

	def get_actions(self, request):
		actions = super(MediaAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	def save_model(self, request, obj, form, change):
		obj.save(request=request)


class PDFAdmin(MediaAdmin):
	list_filter = ['added', 'modified']
	list_display = ['id', 'url', 'type', 'added', 'modified']
	ordering = ['-id']
	raw_id_fields = []
	inlines = []
	fieldsets = (
		(None, {
			'fields': ('id',  'file', 'url', 'type', 'added', 'modified')
		}),
	)
	save_on_top = True

	def save_model(self, request, obj, form, change):
		obj.save(request=request)

@admin.register
class ImageAdmin(MediaAdmin):
	list_filter = ['added', 'modified']
	list_display = ['id', 'thumb', 'added', 'modified']
	ordering = ['-id']
	raw_id_fields = []
	inlines = []
	readonly_fields = ['id', 'thumb', 'preview', 'added', 'modified']
	fieldsets = (
		(None, {
			'fields': ('id', 'preview', 'file', 'url', 'type', 'added', 'modified')
		}),
	)
	save_on_top = True

	def save_model(self, request, obj, form, change):
		obj.save(request=request)


admin.site.register(PDF, PDFAdmin)
admin.site.register(Image)
