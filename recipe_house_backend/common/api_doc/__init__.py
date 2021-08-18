from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

get_schema_view(
    openapi.Info(
        title="Nirvana API",
        default_version='v1',
        description="Nirvana API for Claims and Coverage",
        contact=openapi.Contact(email="urvish@meetnirvana.com"),
        license=openapi.License(name="Proprietary Software"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
