from django.urls import (
    include,
    path
)
from libraries import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'publishers', views.PublisherViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'borrowed_books', views.BorrowedBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
