from django.contrib.auth.models import (
    User,
)

from rest_framework import serializers

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


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=50)
    date_birth = serializers.DateField(required=False)

    class Meta:
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
        # alternatywa do usunięcia walidatora unikalności (usuwa wszystkie walidatory - nie do końca dobre rozwiązanie)
        extra_kwargs = {
            'name': {'validators': []},
        }


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'validators': []},
        }


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        # depth = 2


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)
    categories = CategorySerializer(many=True)
    publisher = PublisherSerializer(many=False)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categories', 'publisher', 'publication_year', 'description', 'review']

    def create(self, validated_data):
        # dla many to one
        author = validated_data.pop('author')

        name = author['name']
        surname = author['surname']
        date_birth = author.get('date_birth', '')

        # To jest inny rodzaj zapisu get_or_create
        # try:
        #     author = Author.objects.get(name=name, surname=surname)
        # except Author.DoesNotExist:
        #     author = Author.objects.create(name=name, surname=surname, birth_date=birth_date)

        # zapis zapobiegnie stworzenie duplikatu
        author, created = Author.objects.get_or_create(name=name, surname=surname, defaults={'date_birth': date_birth})
        validated_data['author'] = author

        publisher = validated_data.pop('publisher')
        name = publisher['name']
        publisher, created = Publisher.objects.get_or_create(name=name)
        validated_data['publisher'] = publisher

        # many do many jest wirtualnym polem, więc musze je usunąć przed stworzeniem book
        categories = validated_data.pop('categories')

        book = Book.objects.create(**validated_data)

        # dla many to many
        for category in categories:
            name = category['name']
            category, created = Category.objects.get_or_create(name=name)
            book.categories.add(category)

        return book

    def update(self, instance, validated_data):
        instance.title =
        instance.author = validated_data.get('author', instance.entry)
        instance.publisher = validated_data.get('publisher', instance.rating)
        instance.save()

        return instance






