from django.contrib.auth.models import (
    User,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    filters
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    BasePermission,
    AllowAny
)
from libraries.models import (
    Book,
    Author,
    Category,
    Publisher,
    Review,
    BorrowedBook
)
from libraries.serializers import (
    UserSerializer,
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer,
    ReviewSerializer,
    BorrowedBookSerializer
)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def check_permissions(self, request):
        if self.action in ('create', ) and self.request.user.is_authenticated:
            return self.permission_denied(request)
        elif self.action in ('update', ) and not (self.request.user.is_superuser or self.request.user.is_staff):
            return self.permission_denied(request)
        elif self.action in ('destroy', ) and not self.request.user.is_superuser:
            return self.permission_denied(request)
        else:
            return super().check_permissions(request)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(id=user.id)
        # super wywołuje metode get_queryset z nadrzędengo modelu ModelViewSet


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
    # authentication_classes = (TokenAuthentication,)  # wymiennie, jeśli w stetings nie ustawie globalnie
    permission_classes = (IsAuthenticatedOrReadOnly,)  # w settings jest AllowAny,

    def check_permissions(self, request):
        if self.action in ('create', 'update') and not (self.request.user.is_superuser or self.request.user.is_staff):
            return self.permission_denied(request)
        elif self.action in ('destroy', ) and not self.request.user.is_superuser:
            return self.permission_denied(request)
        else:
            return super().check_permissions(request)


class PermissionForStaffOrSuperuser(BasePermission):
    def has_permission(self, request, view):  # view to jest self w ViewSet
        if view.action in ('create', 'update', 'destroy') and not (request.user.is_staff or request.user.is_superuser):
            return False
        return True


class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, PermissionForStaffOrSuperuser)


class AuthorViewSet(BaseModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ['name', 'surname']
    search_fields = ['name', 'surname']


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']


class PublisherViewSet(BaseModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book', 'rating', 'entry']
    search_fields = ['book', 'rating', 'entry']
    ordering_fields = ['book', 'rating', 'entry']
    ordering = ('book', 'entry',)
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def check_permissions(self, request):
        if self.action in ('create', ) and not (
                self.request.user or self.request.user.is_staff or self.request.user.is_superuser
        ):
            return self.permission_denied(request)
        elif self.action in ('update', 'destroy') and not (
                self.request.user.is_staff or self.request.user.is_superuser
        ):
            return self.permission_denied(request)  # zwraca brak uprawnień
        else:
            return super().check_permissions(request)  # wywołuje standardowe funkcje


class BorrowedBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['book']
    search_fields = ['book__title']

    def check_permissions(self, request):
        if self.action in ('list', 'retrieve') and not self.request.user.is_authenticated:
            return self.permission_denied(request)
        elif self.action in ('create', 'update', 'destroy') and not (
            self.request.user.is_staff or self.request.user.is_superuser
        ):
            return self.permission_denied(request)
        else:
            return super().check_permissions(request)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(user_id=user.id)




