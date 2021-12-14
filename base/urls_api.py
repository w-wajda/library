from django.urls import (
    include,
    path
)
from rest_framework import routers
from libraries import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'publishers', views.PublisherViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
