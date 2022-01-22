from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from recipe_house_backend.api.url import urlpatterns as api_urls, api_doc_url

urlpatterns = [
                  path('admin/', admin.site.urls),

              ] + api_urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns = urlpatterns + api_doc_url
