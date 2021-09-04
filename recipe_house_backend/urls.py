from django.contrib import admin
from django.urls import path, include

from recipe_house_backend.api.url import urlpatterns as api_urls

urlpatterns = [
                  path('admin/', admin.site.urls),
              ] + api_urls
