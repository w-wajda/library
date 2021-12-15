from django.contrib.auth.models import (
    User,
)

from django.http.response import HttpResponseNotAllowed

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
        # books = Book.objects.filter(author=1)
        books = Book.objects.all()
        return books

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        author = Author.objects.create(name=request.data['name'],
                                       surname=request.data['surname'],
                                       date_birth=request.data['date_birth'])
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        author = self.get_object()
        author.name = request.data['name']
        author.surname = request.data['surname']
        author.date_birth = request.data['date_birth']
        author.save()
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        author.delete()
        return Response('Author removed')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def dispatch(self, request, *args, **kwargs):
        # if request.method in ('POST', 'PUT', 'DELETE') and not request.user.is_superuser:
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            # return HttpResponseNotAllowed({'Error': 'Aot allowed'})
            # else:
            return super().dispatch(request, *args, **kwargs)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # if self.request.user.is_superuser:
        return super().update(request, *args, **kwargs)
        # else:
        # return HttpResponseNotAllowed({'Error': 'Aot allowed'})
