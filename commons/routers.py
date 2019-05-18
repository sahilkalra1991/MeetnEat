from rest_framework import routers


class NoPrefixSimpleRouter(routers.SimpleRouter):
    """
    Router to use for Routers without any prefix
    """
    routes = [
        # List route.
        routers.Route(
            url=r'^$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        routers.DynamicListRoute(
            url=r'^{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        routers.Route(
            url=r'^{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        routers.DynamicDetailRoute(
            url=r'^{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]
