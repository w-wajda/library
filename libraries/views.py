from django.contrib.auth.models import (
    User,
)

from django.http.response import HttpResponseNotAllowed
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    viewsets,
    filters
)
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from libraries.models import (
    Book,
    Author,
    Category,
    Publisher,
    Review
)

from libraries.serializers import (
    UserSerializer,
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer,
    ReviewSerializer
)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author__surname', 'categories__name']
    search_fields = ['title', 'author__surname', 'author__name', 'categories__name', 'publisher__name', ]
    ordering_fields = ['id', 'title', 'publication_year']
    # ordering_fields = '__all__'
    ordering = ('publication_year', )
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)  # jeśli mamy IsAuthenticated, to musze byc zalgowana tokenem
    permission_classes = (IsAuthenticated, )  # w settings jest AllowAny, wszędzie dostęp, tutaj muszę się autoryzowane

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name', 'surname']
    search_fields = ['name', 'surname']
    pagination_class = LargeResultsSetPagination


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
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    pagination_class = LargeResultsSetPagination


    def dispatch(self, request, *args, **kwargs):
        # if request.method in ('POST', 'PUT', 'DELETE') and not request.user.is_superuser:
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            # return HttpResponseNotAllowed({'Error': 'Not allowed'})
            # else:
            return super().dispatch(request, *args, **kwargs)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    pagination_class = LargeResultsSetPagination


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # if self.request.user.is_superuser:
        return super().update(request, *args, **kwargs)
        # else:
        # return HttpResponseNotAllowed({'Error': 'Not allowed'})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['rating']
    search_fields = ['rating']
    pagination_class = LargeResultsSetPagination

    def dispatch(self, request, *args, **kwargs):
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            return super().dispatch(request, *args, **kwargs)
