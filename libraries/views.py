from django.contrib.auth.models import (
    User,
)
from rest_framework import viewsets
from rest_framework import permissions

from libraries.models import Book
from libraries.serializers import (
    UserSerializer,
    BookSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
