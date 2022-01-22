from django.conf import settings
from django.conf.urls import url
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from recipe_house_backend.apps.favourites.api.v1.urls import favourite_post_router
from recipe_house_backend.apps.post.api.v1.api_views import PostAddMasterData
from recipe_house_backend.apps.post.api.v1.urls import post_router
from recipe_house_backend.apps.users.api.v1.api_views import UserLogin, FirebaseLogin
from recipe_house_backend.apps.users.api.v1.urls import user_router
from recipe_house_backend.apps.rating.api.v1.urls import rating_router

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
router.registry.extend(post_router.registry)
router.registry.extend(favourite_post_router.registry)
router.registry.extend(rating_router.registry)

urlpatterns = [
    url(r'^api/v1/admin/login/$', UserLogin.as_view(), name='login'),
    url(r'^api/v1/firebase/login/$', FirebaseLogin.as_view(), name='firebase-login'),
    url(r'^api/v1/post-master-data/$', PostAddMasterData.as_view(), name='post-master-data'),

    # apps
    url(api_prefix, include(router.urls)),

]

# Swagger API DOC
api_doc_url = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
