from django.conf import settings
from django.conf.urls import url
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

# from recipe_house_backend.apps.file_upload.api.v1.urls import upload_router
from recipe_house_backend.apps.blog.api.v1.urls import blog_router
from recipe_house_backend.apps.users.api.v1.api_views import TokenRefreshView, activate, UserLogin
from recipe_house_backend.apps.users.api.v1.urls import user_router

schema_view = get_schema_view(
    openapi.Info(
        title="Recipe House API Documentation",
        default_version='v1',
        description="API Documentation",
        contact=openapi.Contact(email="info@Test.com"),
        license=openapi.License(name="Proprietary Software"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_prefix = settings.API_PREFIX

router = routers.DefaultRouter()

router.registry.extend(user_router.registry)
router.registry.extend(blog_router.registry)
# router.registry.extend(upload_router.registry)

urlpatterns = [
    # swagger Api doc
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # simpleJWT urls
    # url(r'^api/v1/login/$', TokenObtainView, name='login'),
    url(r'^api/v1/login/$', UserLogin.as_view(), name='login'),
    url(r'^api/v1/token/refresh/$', TokenRefreshView, name='token_refresh'),
    url(r'^api/v1/users/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    # apps
    url(api_prefix, include(router.urls)),

]
