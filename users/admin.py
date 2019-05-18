from django.contrib import admin
from users.models import FoodPreference, UserFoodPreference


class FoodPreferenceAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class UserFoodPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'preference_id')

# Register your models here.
admin.site.register(FoodPreference, FoodPreferenceAdmin)
admin.site.register(UserFoodPreference, UserFoodPreferenceAdmin)
