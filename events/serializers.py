from rest_framework import serializers, fields
from events import models
from users import (
    serializers as user_serializers,
    models as user_models
)


class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Campus
        fields = ('id', 'name', 'description')
        read_only_fields = ('id', 'name', 'description')


class EventLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventLocation
        fields = ('id', 'name', 'description', 'is_public', 'created_at', 'campus')
        read_only_fields = ('id', 'created_at', 'modified_at', 'is_public')

    def to_representation(self, instance):
        data = super(EventLocationSerializer, self).to_representation(instance)
        if instance.campus:
            data['campus'] = CampusSerializer(instance=instance.campus).data
        return data

    def save(self, **kwargs):
        self._validated_data.update({
            'user_id': kwargs.pop('user_id')
        })
        return super(EventLocationSerializer, self).save(**kwargs)


class EventShoppingItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventShoppingItem
        fields = ('id', 'name', 'created_at', 'event', 'user_id', 'amount')
        read_only_fields = ('id', 'created_at', 'modified_at')

    def to_representation(self, instance):
        data = super(EventShoppingItemSerializer, self).to_representation(instance)
        data['creator'] = instance.user_id if instance.user_id else None
        data['bringer'] = instance.bringer_id if instance.bringer_id else None
        data.pop('user_id')
        return data


class EventShoppingItemBringSerializer(serializers.Serializer):
    bring = fields.BooleanField(required=True)

    def save(self, **kwargs):
        item_obj = kwargs.pop('item_obj')
        user_id = kwargs.pop('user_id')
        if self.validated_data.get('bring'):
            # add bringer_id to shopping item object
            item_obj.bringer_id = user_id
        else:
            # remove bringer_id to shopping item object
            item_obj.bringer_id = ""
        item_obj.save()
        return item_obj


class EventMealSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventMeal
        fields = ('id', 'name', 'created_at', 'event', 'meal_id', 'user_id')
        read_only_fields = ('id', 'created_at', 'modified_at')

    def to_representation(self, instance):
        data = super(EventMealSerializer, self).to_representation(instance)
        data['creator'] = instance.user_id
        data['voters'] = instance.votes.values_list('user_id', flat=True)
        data['votes'] = len(data['voters'])
        data.pop('user_id')
        return data


class EventMealVoteSerializer(serializers.Serializer):
    vote = fields.BooleanField(required=True)

    def save(self, **kwargs):
        meal_obj = kwargs.pop('meal_obj')
        user_id = kwargs.pop('user_id')
        if self.validated_data.get('vote'):
            # Create Vote
            meal_obj.votes.create(user_id=user_id)
        else:
            # Delete Vote
            meal_obj.votes.filter(user_id=user_id).delete()
        return meal_obj


class EventMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventMessage
        fields = ('id', 'text', 'user_id', 'event', 'created_at')
        read_only_fields = ('id', 'created_at', 'modified_at')

    def to_representation(self, instance):
        data = super(EventMessageSerializer, self).to_representation(instance)
        data['creator'] = instance.user_id
        data.pop('user_id')
        return data


class EventPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventPreference
        fields = ('event', 'food_preference')

    def to_representation(self, instance):
        return user_serializers.FoodPreferenceSerializer(instance=instance.food_preference).data


class EventUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventUser
        fields = ('event', 'user_id')

    def to_representation(self, instance):
        """
        :param instance: EventUser instance
        :return: UserSerializer data
        """
        return user_serializers.UserSerializer(instance=instance.user_id).data


class EventSerializer(serializers.ModelSerializer):
    preferenceids = fields.MultipleChoiceField(
        choices=user_models.FoodPreference.objects.all().values_list('pk', flat=True),
        allow_null=True,
        required=False,
        help_text="Food Preference IDs to save with event while creation"
    )

    class Meta:
        model = models.Event
        fields = ('id', 'title', 'description', 'start_at', 'end_at', 'created_at', 'capacity', 'user_id', 'location',
                  'preferenceids')
        read_only_fields = ('id', 'created_at', 'user_id')

    def to_representation(self, instance):
        data = super(EventSerializer, self).to_representation(instance)
        data['creator'] = instance.user_id
        data.pop('user_id')
        if self.context.get('is_list', False):
            data['num_members'] = instance.users.count()
            data['members'] = []
            data['shoppingitems'] = []
            data['meals'] = []
            data['messages'] = []
        else:
            data['members'] = instance.users.all().values_list('user_id', flat=True)
            data['num_members'] = len(data['members'])
            data['shoppingitems'] = EventShoppingItemSerializer(instance=instance.shop_items.all(), many=True).data
            data['meals'] = EventMealSerializer(instance=instance.meals.all(), many=True).data
            data['messages'] = EventMessageSerializer(instance=instance.messages.all(), many=True).data

        data['preferences'] = EventPreferenceSerializer(
            instance=instance.preferences.all(),
            many=True
        ).data
        data['location'] = EventLocationSerializer(instance=instance.location).data
        return data

    def save(self, **kwargs):
        """
        Create/Update Event Object.
        Then check is there are preferenceids.
        If yes, Delete old preferences. Create EventPreference objects
        """
        self._validated_data.update({
            'user_id': kwargs.pop('user_id')
        })
        preferenceids = self._validated_data.pop('preferenceids', [])
        event_obj = super(EventSerializer, self).save(**kwargs)
        if preferenceids:
            # Delete Old Preference objects
            models.EventPreference.objects.filter(event=event_obj).delete()
            # Create Event Preference objects
            data = [
                {
                    "event": event_obj.id,
                    "food_preference": pref_id
                } for pref_id in preferenceids
            ]
            pref_serializer = EventPreferenceSerializer(data=data, many=True)
            pref_serializer.is_valid(raise_exception=True)
            pref_serializer.save()

        return event_obj
