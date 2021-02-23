from django.contrib import admin

from config.models import *


def save_all(self, request, queryset):
	if queryset.count() > 0:
		model = type(queryset[0])
		instances = model.objects.all()
		for instance in instances:
			instance.save()
save_all.short_description = "Save all"

def save_selected(modeladmin, request, queryset):
	for instance in queryset:
		instance.save()
save_selected.short_description = "Save selected"

def revert(modeladmin, request, queryset):
	count = queryset.count()
	if count > 1 or count < 1:
		return None
	querset[0].revert()
save_selected.short_description = "Save selected"


class VersionsInlineAdmin(admin.TabularInline):
    model = Version
    verbose_name = "Version"
    verbose_name_plural = "Versions"
    extra = 0
    raw_id_fields = ['setting']
    readonly_fields = ['setting', 'value', 'created', 'revert_button', 'admin_link']
    fields = ['value', 'created', 'admin_link', 'revert_button']


class PrototypeAdmin(admin.ModelAdmin):
	list_filter = []
	list_display = ['id']
	search_fields = []
	list_editable = []
	list_display_links = ['id']
	ordering = ['-id']
	readonly_fields = ['id']
	actions = []
	list_per_page = 30
	raw_id_fields = []
	inlines = []
	fieldsets = (
		(None, {
			'fields': ('id')
		}),
		('Other', {
			'classes': ('collapse',),
			'fields': (),
		}),
	)


class SettingAdmin(admin.ModelAdmin):
	list_filter = ['type', 'folder', 'site']
	list_display = ['id', '__unicode__', 'type', 'site']
	search_fields = ['key']
	list_editable = []
	list_display_links = ['id']
	# ordering = ['folder__name', 'key']
	readonly_fields = ['id', 'preview', '__unicode__']
	actions = []
	list_per_page = 30
	raw_id_fields = ['folder']
	inlines = [VersionsInlineAdmin]
	fieldsets = (
		(None, {
			'fields': ('id', 'type', '__unicode__', 'site', 'folder', 'key', 'value', 'preview')
		}),
	)


class SettingFolderAdmin(admin.ModelAdmin):
	list_filter = ['parent']
	list_display = ['id', '__unicode__']
	search_fields = ['name']
	list_editable = []
	list_display_links = ['id']
	readonly_fields = ['id']
	actions = []
	list_per_page = 30
	raw_id_fields = ['parent']
	inlines = []
	fieldsets = (
		(None, {
			'fields': ('id', 'parent', 'name')
		}),
	)


class VersionAdmin(admin.ModelAdmin):
	list_filter = ['setting__type', 'setting__folder', 'created']
	list_display = ['id', '__unicode__', 'preview', 'created']
	search_fields = ['setting__key']
	list_editable = []
	list_display_links = ['id']
	# ordering = ['folder__name', 'key']
	readonly_fields = ['id', 'preview', '__unicode__', 'setting', 'value', 'created', 'revert_button']
	actions = [revert]
	list_per_page = 30
	raw_id_fields = []
	inlines = []
	fieldsets = (
		(None, {
			'fields': ('id', '__unicode__', 'created', 'value', 'preview',)
		}),
	)


admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingFolder, SettingFolderAdmin)
admin.site.register(Version, VersionAdmin)
