from django.contrib import admin
from django.urls import (
    include,
    path
)
from base import urls_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls_api)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
