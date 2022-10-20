from rest_framework import (
    mixins,
    status
)
from rest_framework.response import Response

from commons import views as common_views
from users import (
    models,
    serializers
)


class FoodPreferenceView(
    mixins.ListModelMixin,
    common_views.BaseGenericViewSet
):
    """
    Class which contain all REST APIs related to Food Preferences
    """
    model = models.FoodPreference
    serializer_class = serializers.FoodPreferenceSerializer
    queryset = models.FoodPreference.objects.all()


class UserFoodPreferenceView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    common_views.AuthBaseGenericViewSet
):
    """
    Class which contain all REST APIs related to Food preferences of User
    """
    model = models.FoodPreference
    serializer_class = serializers.FoodPreferenceSerializer
    create_serializer_class = serializers.UserFoodPreferenceSerializer

    def get_queryset(self):
        return models.FoodPreference.objects.filter(users__user_id=self.user_id)

    @property
    def user_id(self):
        return self.request.user.user_id

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.serializer_class(instance=self.get_queryset(), many=True).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(user_id=self.user_id)
