from rest_framework.permissions import IsAuthenticated

from commons.authentication import FBLAuthentication


class ActionSerializerAPIMixin(object):
    """
    This mixin is used to add provision for using a different serializer for every action of an API
    Add this mixin and define <action>_serializer_class attribute in API, which will used for respective <action>
    """
    def get_serializer_class(self):
        return getattr(self, '{0}_serializer_class'.format(self.action.lower())) if \
            self.action and getattr(self, '{0}_serializer_class'.format(self.action.lower()), None) \
            else super(ActionSerializerAPIMixin, self).get_serializer_class()


class AuthRequiredMixin(object):
    authentication_classes = [FBLAuthentication]
    permission_classes = [IsAuthenticated]


class CustomResponseFormatMixin(object):
    """
    Maybe used in future to standardise the Responses
    """
