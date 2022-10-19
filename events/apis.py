from _datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models.query_utils import Q

from rest_framework import (
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from commons import views as common_views
from events import (
    models,
    serializers
)


class UserEventMatchView(
    mixins.ListModelMixin,
    common_views.BaseGenericViewSet
):
    """
    Class which contain all REST APIs related to Event Matches of a User
    """
    model = models.Event
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()[:1]

    def get_serializer_context(self):
        context = super(UserEventMatchView, self).get_serializer_context()
        context.update({
            'is_list': True
        })
        return context


class EventView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    common_views.AuthBaseGenericViewSet
):
    """
    Class which contain all REST APIs related to Events
    list: Returns all user's events
    all: Returns all available events
    """
    model = models.Event
    serializer_class = serializers.EventSerializer
    users_serializer_class = serializers.EventUserSerializer
    messages_serializer_class = serializers.EventMessageSerializer
    meals_serializer_class = serializers.EventMealSerializer
    shoppingitems_serializer_class = serializers.EventShoppingItemSerializer
    queryset = models.Event.objects.prefetch_related('users', 'preferences', 'messages', 'shop_items', 'meals').all()

    @property
    def user_id(self):
        return self.request.user.user_id if self.request.user.is_authenticated else None

    def get_queryset(self):
        if self.action.lower() not in ["join", "leave"]:
            return self.queryset.filter(users__user_id=self.user_id)
        else:
            return self.queryset

    @action(detail=False, permission_classes=[])
    def all(self, request, *args, **kwargs):
        """
        Returns all available events
        Or 
        Return Matched events if following params are passed:
        1. campus: Campus of the event
        2. start_at: start datetime
        3. end_at: end datetime
        4. preferences: list of food preferences
        """
        queryset = self.queryset
        campus_ids = request.query_params.getlist('campus', None)
        preference_slugs = request.query_params.getlist('preferences', None)
        start_at = datetime.strptime(
            request.query_params.get('start_at'),
            settings.REST_FRAMEWORK['DATETIME_FORMAT']
        ) if request.query_params.get('start_at', None) else None
        end_at =  datetime.strptime(
            request.query_params.get('end_at'),
            settings.REST_FRAMEWORK['DATETIME_FORMAT']
        ) if request.query_params.get('end_at', None) else None

        if campus_ids or preference_slugs or start_at or end_at:
            # Get Matched Events
            query_params = Q()
            if campus_ids:
                query_params = query_params & Q(location__campus_id__in=campus_ids)
            if preference_slugs:
                query_params = query_params & Q(preferences__food_preference__slug__in=preference_slugs)
            if start_at and end_at:
                # Both Start and End time are specified
                # Filter Events which lie between the time period
                query_params = query_params & Q(start_at__gte=start_at) & Q(end_at__lte=end_at)
            elif start_at:
                # Start at is specified
                # Return events which start on the same date after this time
                query_params = query_params & Q(start_at__contains=start_at.date()) & Q(start_at__gte=start_at)
            elif end_at:
                # End at is specified
                # Return events which end on the same date before this time
                query_params = query_params & Q(end_at__contains=end_at.date()) & Q(end_at__lte=end_at)

            if self.user_id:
                # Exclude the events User has joined or created
                queryset = queryset.exclude(users__user_id=self.user_id)

            queryset = queryset.filter(query_params).distinct()
        else:
            # Get All Events
            queryset = self.queryset

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """
        Add a user to the event
        Returns new user of the Event
        """
        event_obj = self.get_object()
        user_id = self.user_id
        try:
            event_user = event_obj.users.get(user_id=user_id)
        except ObjectDoesNotExist:
            # Create a Event user object on POST
            users_serializer = self.users_serializer_class(data={
                'event': event_obj.id,
                'user_id': user_id
            })

            users_serializer.is_valid(raise_exception=True)
            event_user = users_serializer.save()
        return Response(
            self.users_serializer_class(instance=event_user).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def leave(self, request, *args, **kwargs):
        """
        Delete a user from the event
        Returns code 204
        """
        event_obj = self.get_object()
        user_id = self.user_id
        models.EventUser.objects.filter(event=event_obj, user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post'])
    def messages(self, request, *args, **kwargs):
        """
        GET: List all messages of a group
        POST: Create new message for a group
        """
        event_obj = self.get_object()
        if request.method.lower() == "get":
            return Response(
                self.messages_serializer_class(instance=event_obj.messages.all(), many=True).data
            )
        else:
            data = request.data.copy()
            data['user_id'] = self.user_id
            data['event'] = event_obj.id
            messages_serializer = self.messages_serializer_class(data=data)
            messages_serializer.is_valid(raise_exception=True)
            event_message = messages_serializer.save()
            return Response(
                self.messages_serializer_class(instance=event_message).data,
                status=status.HTTP_201_CREATED
            )

    @action(detail=True, methods=['get', 'post'])
    def meals(self, request, *args, **kwargs):
        """
        GET: List all meals of a group
        POST: Create new meal for a group
        """
        event_obj = self.get_object()
        if request.method.lower() == "get":
            return Response(
                self.meals_serializer_class(instance=event_obj.meals.all(), many=True).data
            )
        else:
            data = request.data.copy()
            data['user_id'] = self.user_id
            data['event'] = event_obj.id
            meals_serializer = self.meals_serializer_class(data=data)
            meals_serializer.is_valid(raise_exception=True)
            event_meal = meals_serializer.save()
            return Response(
                self.meals_serializer_class(instance=event_meal).data,
                status=status.HTTP_201_CREATED
            )

    @action(detail=True, methods=['get', 'post'])
    def shoppingitems(self, request, *args, **kwargs):
        """
        GET: List all Shopping items of a group
        POST: Create new Shopping Item for a group
        """
        event_obj = self.get_object()
        if request.method.lower() == "get":
            return Response(
                self.shoppingitems_serializer_class(instance=event_obj.shop_items.all(), many=True).data
            )
        else:
            data = request.data.copy()
            data['user_id'] = self.user_id
            data['event'] = event_obj.id
            shoppingitems_serializer = self.shoppingitems_serializer_class(data=data)
            shoppingitems_serializer.is_valid(raise_exception=True)
            event_shoppingitem = shoppingitems_serializer.save()
            return Response(
                self.shoppingitems_serializer_class(instance=event_shoppingitem).data,
                status=status.HTTP_201_CREATED
            )

    def perform_create(self, serializer):
        serializer.save(user_id=self.user_id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.user_id)

    def get_serializer_context(self):
        context = super(EventView, self).get_serializer_context()
        context.update({
            'is_list': self.action == 'list' or self.action == 'all',
        })
        return context


class EventMessageView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    common_views.AuthBaseGenericViewSet
):
    """
    Class for API to Retrieve and delete an event message
    """
    model = models.EventMessage
    serializer_class = serializers.EventMessageSerializer
    queryset = models.EventMessage.objects.all()


class EventShoppingItemView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    common_views.AuthBaseGenericViewSet
):
    """
    Class for API to Retrieve and delete an event shopping item
    """
    model = models.EventShoppingItem
    serializer_class = serializers.EventShoppingItemSerializer
    bring_serializer_class = serializers.EventShoppingItemBringSerializer
    queryset = models.EventShoppingItem.objects.all()

    @property
    def user_id(self):
        return self.request.user.user_id

    @action(detail=True, methods=['post'])
    def bring(self, request, *args, **kwargs):
        """
        User brings ShoppingItem 
        Returns ShoppingItem Object
        """
        item_obj = self.get_object()
        save_data = {
            'user_id': self.user_id,
            'item_obj': item_obj
        }
        bring_serializer = self.bring_serializer_class(data=self.request.data)
        bring_serializer.is_valid(raise_exception=True)
        bring_serializer.save(**save_data)

        return Response(
            self.serializer_class(instance=item_obj).data,
        )


class EventMealView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    common_views.AuthBaseGenericViewSet
):
    """
    Class for API to Retrieve and delete an event meal
    """
    model = models.EventMeal
    serializer_class = serializers.EventMealSerializer
    vote_serializer_class = serializers.EventMealVoteSerializer
    queryset = models.EventMeal.objects.all()

    @property
    def user_id(self):
        return self.request.user.user_id

    @action(detail=True, methods=['post'])
    def vote(self, request, *args, **kwargs):
        """
        User Vote/DeVote on a meal
        Returns Meal Object
        """
        meal_obj = self.get_object()
        save_data = {
            'user_id': self.user_id,
            'meal_obj': meal_obj
        }
        vote_serializer = self.vote_serializer_class(data=self.request.data)
        vote_serializer.is_valid(raise_exception=True)
        vote_serializer.save(**save_data)

        return Response(
            self.serializer_class(instance=meal_obj).data,
        )


class EventLocationView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    common_views.AuthBaseGenericViewSet
):
    """
    Class which contain all REST APIs related to Event Locations
    all: Returns all  public event locations
    list: Returns all user's private event locations
    """
    model = models.EventLocation
    serializer_class = serializers.EventLocationSerializer

    @property
    def user_id(self):
        return self.request.user.user_id

    def get_queryset(self):
        return models.EventLocation.objects.filter(user_id=self.user_id)

    @action(detail=False, authentication_classes=[], permission_classes=[])
    def all(self, request, *args, **kwargs):
        """
        Returns all Public event locations
        """
        serializer = self.get_serializer(models.EventLocation.objects.filter(is_public=True), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user_id=self.user_id)


class CampusView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    common_views.BaseGenericViewSet
):
    """
    Class for Campus APIs 
    """
    model = models.Campus
    serializer_class = serializers.CampusSerializer
    queryset = models.Campus.objects.all()
