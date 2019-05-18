from django.contrib import admin
from events import models


class EventMessageInline(admin.TabularInline):
    model = models.EventMessage


class EventShoppingItemInline(admin.TabularInline):
    model = models.EventShoppingItem


class EventUserInline(admin.TabularInline):
    model = models.EventUser


class EventMealInline(admin.TabularInline):
    model = models.EventMeal


class EventPreferenceInline(admin.TabularInline):
    model = models.EventPreference


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'start_at', 'end_at', 'user_id')
    inlines = [
        EventUserInline,
        EventMessageInline,
        EventPreferenceInline,
        EventMealInline,
        EventShoppingItemInline
    ]


class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_public', 'campus')


class CampusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Register your models here.
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Campus, CampusAdmin)
admin.site.register(models.EventLocation, EventLocationAdmin)
