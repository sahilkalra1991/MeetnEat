"""
Use this File to define Base Views and Viewsets, which will be used by Various APIs.
This File can then be used to define categories of APIs and add Common functionality to All of APIs
NOTE: Do not use any View of Rest framwork
"""
from rest_framework import viewsets, views, generics
from commons import mixins as common_mixins


class BaseGenericViewSet(
    common_mixins.CustomResponseFormatMixin,
    common_mixins.ActionSerializerAPIMixin,
    viewsets.GenericViewSet
):
    """
    Base class to be used by all ViewSets
    """
    lookup_value_regex = '[0-9]+'


class AuthBaseGenericViewSet(
    common_mixins.AuthRequiredMixin,
    BaseGenericViewSet
):
    """
    Base Class to use for Viewsets which require user to be authenticated
    """


class BaseApiView(
    common_mixins.CustomResponseFormatMixin,
    views.APIView
):
    """
    Base class to be used by all ApiViews
    """


class AuthBaseApiView(
    common_mixins.AuthRequiredMixin,
    BaseApiView
):
    """
    Base Class to use for APiView which require user to be authenticated
    """


class BaseGenericApiView(
    common_mixins.CustomResponseFormatMixin,
    generics.GenericAPIView
):
    """
    Base class to be used by all GenericApiViews
    """


class AuthBaseGenericApiView(
    common_mixins.AuthRequiredMixin,
    BaseGenericApiView
):
    """
    Base Class to use for GenericApiView which require user to be authenticated
    """
