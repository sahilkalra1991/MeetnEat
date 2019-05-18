import random
from rest_framework import serializers
from users.models import FoodPreference, UserFoodPreference


class UserSerializer(serializers.Serializer):
    fields = ('id', 'name')

    def to_representation(self, instance):
        user_id = str(instance)
        data = {
            'id': user_id
        }
        return data


class FoodPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodPreference
        fields = ('id', 'slug', 'name')


class UserFoodPreferenceSerializer(serializers.Serializer):
    preferences = serializers.ListField()

    def is_valid(self, raise_exception=False):
        super(UserFoodPreferenceSerializer, self).is_valid()

    def save(self, **kwargs):
        user_id = kwargs.get('user_id')
        # Delete old preferences and add new ones
        UserFoodPreference.objects.filter(user_id=user_id).delete()
        for preference in self.data.get('preferences', ()):
            try:
                food_pref = FoodPreference.objects.get(slug=preference['slug'])
            except FoodPreference.ObjectNotFound:
                food_pref = None
            else:
                UserFoodPreference.objects.get_or_create(user_id=user_id, preference=food_pref)
