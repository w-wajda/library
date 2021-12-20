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

    def update(self, instance, validated_data):
        instance.entry = validated_data.get('entry', instance.entry)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()

        return instance


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)
    # categories = PrimaryKeyRelatedField(many=True, read_only=True)
    categories = CategorySerializer(many=True)
    publisher = PublisherSerializer(many=False)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categories', 'publisher', 'publication_year', 'description', 'review']

    def create(self, validated_data):
        categories = validated_data['categories']
        del validated_data['categories']

        # dla many to one
        author = validated_data.pop('author')
        author = Author.objects.create(**author)
        validated_data['author'] = author

        publisher = validated_data.pop('publisher')
        publisher = Publisher.objects.create(**publisher)
        validated_data['publisher'] = publisher

        book = Book.objects.create(**validated_data)

        # dla many to many
        for category in categories:
            print(category)
            c = Category.objects.create(**category)
            book.categories.add(c)

        book.save()

        return book

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.entry)
        instance.publisher = validated_data.get('publisher', instance.rating)
        instance.save()

        return instance






