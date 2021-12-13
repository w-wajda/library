from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name='Name')
    surname = models.CharField(max_length=50, verbose_name='Surname')
    date_birth = models.DateField(verbose_name='Date of birth')

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
    publication_year = models.PositiveSmallIntegerField(verbose_name='Publication year')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.title













