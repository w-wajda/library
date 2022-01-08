from datetime import date

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=User)  # dekorator, który nasłuchuje zapisy użytkownika, następnie wsyła mail powitalny
def send_welcome_email(sender, instance: User, created=False, **kwargs):
    if created and instance.email:  # jeśli użytkownik został stworzony, instacja to user, stad instance.email
        send_mail('Welcome in Library', f'Thanks for your registration. Your account details: \n'
                                        f'Login - {instance.username} \n'
                                        f'Best regards, \nYour Library', from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[instance.email])


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
    author = models.ForeignKey(Author, verbose_name='Author', on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, verbose_name='Categories', related_name='books')
    # related_name='books' - tworzy się relacja odwrotna
    publisher = models.ForeignKey(Publisher, verbose_name='Publisher', on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveSmallIntegerField(verbose_name='Publication year')
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    book_cover = models.ImageField(verbose_name='Book cover', upload_to='covers', null=True, blank=True)

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
    date_review = models.DateTimeField(verbose_name='Date of review', default=timezone.now, editable=False)

    def __str__(self):
        return self.book.title

    class Meta:
        ordering = ('-entry', )


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


@receiver(post_save, sender=BorrowedBook)  # dekorator, który nasłuchuje i wsyła mail z informacją o rezerwacji książki
def send_notification_email(sender, instance: BorrowedBook, created=False, **kwargs):
    if created and instance.user.email:
        send_mail('A borrowed book', f'In day {instance.book.title}, You have borrowed the book {instance.book.title}. '
                                     f'Remember to return to {instance.date_end}.\n'
                                     f'Best regards, \nYour Library', from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[instance.user.email])











