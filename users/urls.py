from rest_framework import routers
from users import apis

user_routers = routers.SimpleRouter()

user_routers.register('preferences/all', apis.FoodPreferenceView, 'preference')
user_routers.register('preferences', apis.UserFoodPreferenceView, 'user_preference')

urlpatterns = user_routers.urls
