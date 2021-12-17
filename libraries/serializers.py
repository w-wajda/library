from django.contrib.auth.models import (
    User,
)
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ListSerializer

from libraries.models import (
    Book,
    Author,
    Category,
    Publisher,
    Review
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'surname', 'date_birth']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class BookMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']


class ReviewSerializer(serializers.ModelSerializer):
    book = BookMiniSerializer(many=False)

    class Meta:
        model = Review
        fields = '__all__'
        # depth = 2


class BookSerializer(serializers.ModelSerializer):
    author = CategorySerializer(many=False)
    # categories = PrimaryKeyRelatedField(many=True, read_only=True)
    categories = CategorySerializer(many=True)
    publisher = PublisherSerializer(many=False)
    review = ReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categories', 'publisher', 'publication_year', 'description', 'review']








