from django.urls import (
    include,
    path
)
from rest_framework import routers
from libraries import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
