from django.contrib.auth.models import (
    User,
)
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from libraries.models import (
    Book,
    Author,
    Category,
    Publisher,
    Review,
    BorrowedBook
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email']
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True, 'validators': [UniqueValidator(queryset=User.objects.all())]}
        }  # hasło wymagane, nie zostanie pokazane, obowiązkowe imie, nazwisko i mail (mail unikatowy)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # utworzenie user
        Token.objects.create(user=user)  # utworzenie tokena
        return user


class ShortAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'surname']


class ShortBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']


class SimpleAuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']


class ShortCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ShortPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class ShortReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'entry', 'date_review']


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=50)
    date_birth = serializers.DateField(required=False)
    books = ShortBookSerializer(many=True)

    class Meta:
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    books = SimpleAuthorBookSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'books']
        # alternatywa do usunięcia walidatora unikalności (usuwa wszystkie walidatory - nie do końca dobre rozwiązanie)
        extra_kwargs = {
            'name': {'validators': []},  # extra_kwargs dodatkowe argumenty do fields
        }


class PublisherSerializer(serializers.ModelSerializer):
    books = SimpleAuthorBookSerializer(many=True)

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'books']
        extra_kwargs = {
            'name': {'validators': []},
        }


class ReviewSerializer(serializers.ModelSerializer):
    book = SimpleAuthorBookSerializer(many=False)

    class Meta:
        model = Review
        fields = ['id', 'book', 'rating', 'entry', 'date_review']
        # depth = 2


class DateEndBorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['id', 'date_end']


class BorrowedBookSerializer(serializers.ModelSerializer):
    # book = BookSerializer(many=False)
    # user = UserSerializer(many=False)

    class Meta:
        model = BorrowedBook
        fields = ['id', 'user', 'book', 'date_start', 'date_end']


class BookSerializer(serializers.ModelSerializer):
    author = ShortAuthorSerializer(many=False)
    categories = ShortCategorySerializer(many=True)
    publisher = ShortPublisherSerializer(many=False)
    review = ShortReviewSerializer(many=True, read_only=True)
    # date_end_borrowed_book = DateEndBorrowedBookSerializer(many=True, source='borrowed')  # book.borrowed.all()
    day_of_return = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categories', 'publisher', 'publication_year', 'description', 'review',
                  'day_of_return']

    def get_day_of_return(self, obj: Book):
        """
        last_borrowed = obj.borrowed.order_by('-date_end')[0] - w przypadku gdy nie bedziemy miec wypozyczenia to
        wywali sie IndexError. Chcemy temu zapobiec.Mozemy zrobic try, except ALBO uzyc .first() na querysecie
        np. obj.borrowed.order_by('-date_end').first() - zwroci nam obiket BorrowedBook albo None
        """
        last_borrowed = obj.borrowed.order_by('-date_end').first()
        if last_borrowed:
            return last_borrowed.date_end
        else:
            return None

    def create(self, validated_data):  # tworzony create bo mamy get or create, a autora mamy unikalnego
        # dla many to one
        author = validated_data.pop('author')
        name = author['name']
        surname = author['surname']
        date_birth = author.get('date_birth')

        # Inny rodzaj zapisu get_or_create
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

    def update(self, instance: Book, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)
        instance.description = validated_data.get('description', instance.description)

        if 'author' in validated_data:
            author = validated_data.get('author')

            name = author['name']
            surname = author['surname']
            date_birth = author.get('date_birth')
            author, created = Author.objects.get_or_create(name=name, surname=surname,
                                                           defaults={'date_birth': date_birth})
            instance.author = author

        if 'categories' in validated_data:
            categories = validated_data.get('categories')

            new_categories = []
            for category in categories:
                name = category['name']
                category, created = Category.objects.get_or_create(name=name)

                # pk = id
                new_categories.append(category.pk)
                instance.categories.add(category)

            old_categories = instance.categories.exclude(pk__in=new_categories)
            instance.categories.remove(*old_categories)

        if 'publisher' in validated_data:
            publisher = validated_data.get('publisher')

            name = publisher['name']
            publisher, created = Publisher.objects.get_or_create(name=name)

            instance.publisher = publisher

        instance.save()

        return instance




