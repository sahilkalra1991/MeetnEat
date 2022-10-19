from rest_framework import routers
from events import apis

event_routers = routers.SimpleRouter()

event_routers.register('', apis.EventView, 'event')
event_routers.register('locations', apis.EventLocationView, 'location')
event_routers.register('campuses', apis.CampusView, 'campuses')
event_routers.register('matches', apis.UserEventMatchView, 'event_match')
event_routers.register('messages', apis.EventMessageView, 'event_messages')
event_routers.register('meals', apis.EventMealView, 'event_meals')
event_routers.register('shoppingitems', apis.EventShoppingItemView, 'event_items')

urlpatterns = event_routers.urls
