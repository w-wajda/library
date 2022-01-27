from django.db import models


class BookQuerySet(models.QuerySet):

    def modern(self):
        return self.filter(publication_year__gte=2019)

    def classic(self):
        return self.filter(publication_year__lt=2019)

    def austen_author(self):
        return self.filter(author__surname='Austen')

    def walter_author(self):
        return self.filter(author__surname='Walter')

    def romans(self):
        return self.filter(categories=1)

    def social_and_moral(self):
        return self.filter(categories=2)

    def black_publisher(self):
        return self.filter(publisher=2)

    def proszynski_publisher(self):
        return self.filter(publisher=1)


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)  # arg. przekazuje jaki model: "book" i z bazy danych z settings

    def modern(self):
        return self.get_queryset().modern()  # get_queryset z bookmanager, modern z bookquweryset

    def classic(self):
        return self.get_queryset().classic()

    def austen_author(self):
        return self.get_queryset().austen_author()

    def walter_author(self):
        return self.get_queryset().walter_author()

    def romans(self):
        return self.get_queryset().romans()

    def social_and_moral(self):
        return self.get_queryset().social_and_moral()

    def black_publisher(self):
        return self.get_queryset().black_publisher()

    def proszynski_publisher(self):
        return self.get_queryset().proszynski_publisher()


class AuthorQuerySet(models.QuerySet):

    def date_birth_author(self):
        return self.filter(date_birth='1775-12-16')


class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorQuerySet(self.model, using=self._db)

    def date_birth_author(self):
        return self.get_queryset().date_birth_author()


"""Inny sposób na zapis"""
# class BookModernManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(publication_year__gte=2019)  # większe bądź równe
#
#
# class BookClassicManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(publication_year__lt=2019)  # mniejsze niż 2019
#
#
# class BookAustenManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(author__surname='Austen')
#
#
# class BookWalterManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(author__surname='Walter')
