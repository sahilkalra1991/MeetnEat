"""foodgroups URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from django.contrib import admin

from rest_framework.schemas import get_schema_view
from rest_framework import permissions


from drf_yasg import (
    openapi,
    views as drf_yasg_views
)

docs_schema = drf_yasg_views.get_schema_view(
    openapi.Info(
        title="Meet'n'Eat API",
        default_version="v1",
        description="Swagger UI documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(('users.urls', 'users'), namespace="user_api")),
    re_path(r'^api/events/', include(('events.urls', 'events'), namespace="event_api")),
    re_path(r'^api/openapi/', get_schema_view(title="Meet'n'Eat API")),
    re_path(r'^api/docs/$', docs_schema.with_ui("swagger", cache_timeout=0)),
    re_path(r'^api/redocs/', docs_schema.with_ui("redoc", cache_timeout=0)),
]
