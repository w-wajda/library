from datetime import date

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from libraries.managers import (
    BookManager,
)


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name='Name')
    surname = models.CharField(max_length=50, verbose_name='Surname')
    date_birth = models.DateField(verbose_name='Date of birth', null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        unique_together = [['name', 'surname']]
        ordering = ('date_birth', )


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', unique=True)
    author = models.ForeignKey(Author, verbose_name='Author', on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, verbose_name='Categories', related_name='books')
    # related_name='books' - tworzy się relacja odwrotna
    publisher = models.ForeignKey(Publisher, verbose_name='Publisher', on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveSmallIntegerField(verbose_name='Publication year')
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    book_cover = models.ImageField(verbose_name='Book cover', upload_to='covers', null=True, blank=True)

    objects = models.Manager()  # można zamienić models.Manager() na BookManager(), żeby było jedno jak sie ma wszystko
    books = BookManager()
    """Inny sposób zapisu """
    # modern_books = BookModernManager()
    # old_books = BookClassicManager()
    # austen_books = BookAustenManager()
    # walter_books = BookWalterManager()

    def __str__(self):
        return self.title

    class Meta:
        # db_table = 'books'
        order_with_respect_to = 'author'


class Review(models.Model):
    BAD = 0
    NOT_TO_BAD = 1
    GOOD = 2
    VERY_GOOD = 3
    FANTASTIC = 4

    RATING = (
        (BAD, 'Bad'),
        (NOT_TO_BAD, 'Not to bad'),
        (GOOD, 'Good'),
        (VERY_GOOD, 'Very_good'),
        (FANTASTIC, 'Fantastic')
    )

    book = models.ForeignKey(Book, verbose_name='Book', on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(verbose_name='Rating', choices=RATING)
    entry = models.TextField(verbose_name='Entry', null=True, blank=True)
    date_review = models.DateTimeField(verbose_name='Date of review', default=timezone.now, editable=False)

    def __str__(self):
        return self.book.title

    class Meta:
        ordering = ('-date_review', )


def check_if_borrowed(book_id):
    if isinstance(book_id, Book):  # sprawdzenie czy book_id jest instancją Book
        obj = book_id
    else:
        obj = Book.objects.get(pk=book_id)

    if obj.borrowed.all().filter(date_end__gt=date.today()):
        raise ValidationError('This book is borrowed')


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Book', on_delete=models.CASCADE, related_name='borrowed',
                             validators=[check_if_borrowed])  # validator sprawdzający pożyczoną książkę
    date_start = models.DateField(verbose_name='Date borrowed', default=timezone.now, editable=True)
    date_end = models.DateField(verbose_name='Date return', default=timezone.now() + timezone.timedelta(days=30),
                                editable=True)

    def __str__(self):
        return f'{self.book.title} {self.date_end}'

    class Meta:
        ordering = ('-date_end', )














