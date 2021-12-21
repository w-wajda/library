from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name='Name')
    surname = models.CharField(max_length=50, verbose_name='Surname')
    date_birth = models.DateField(verbose_name='Date of birth', null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        unique_together = [['name', 'surname']]


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
    author = models.ForeignKey(Author, verbose_name='Author', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, verbose_name='Categories')
    publisher = models.ForeignKey(Publisher, verbose_name='Publisher', on_delete=models.CASCADE)
    publication_year = models.PositiveSmallIntegerField(verbose_name='Publication year', null=True, blank=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True)

    def __str__(self):
        return self.title


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
    date_review = models.DateTimeField(verbose_name='Date of review', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.book.title















