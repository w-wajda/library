from django.contrib.auth.models import (
    User,
)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from libraries.models import (
    Book,
    Author,
    Category,
    Publisher
)

from libraries.serializers import (
    UserSerializer,
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.filter(author=1)
        return books

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer





