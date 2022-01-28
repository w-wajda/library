from django.test import TestCase

from django.urls import reverse, resolve

from libraries.models import Author, Book, Publisher, Category
from libraries.models import check_if_borrowed


class LibrariesTests(TestCase):

    # models test
    def setUp(self):  # stworzony setUp aby przy kolejnych testach nie tworzyć nowych Author
        self.author = Author.objects.create(name='Imie', surname='Nazwisko', date_birth='1775-12-16')
        self.publisher = Publisher.objects.create(name='Test')
        self.category = Category.objects.create(name='Test')
        self.book = Book.objects.create(title='Test', author=self.author, publisher=self.publisher,
                                        publication_year=2019)
        self.book.categories.add(self.category)

    def test_modern_book(self):
        modern_books = Book.books.modern()
        self.assertTrue(self.book in modern_books)

    def test_model_author_as_text(self):
        self.assertEqual(str(self.author), 'Imie Nazwisko')  # test sprawdza, czy jest prawidłowo sformatowany __str__

    def test_author_is_not_null(self):
        self.assertNotEqual(self.author, None)  # test sprawdza, czy nie jest pusty

    def test_author_is_unique(self):
        with self.assertRaises(Exception):
            self.author = Author.objects.create(name='Imie', surname='Nazwisko')  # test sprawdza unikatowość

    # models manager test
    def test_if_manager(self):
        authors = Author.author.date_birth_author()
        self.assertGreater(len(authors), 0)  # test sprawdza ile jest takich rekordów, czy jest więcej niż 0

    # def test
    def test_function_check_if_borrowed_is_working(self):
        pass

    # test TDD Test driven development

    def test_book_method_is_modern(self):
        """powinna zwrócić True, jeśli rok jest większa niż 2000"""
        self.assertTrue(self.book.is_modern())

    def test_book_method_is_not_modern(self):
        """powinna zwrócić False, jeśli rok jest mniejszy lub równy 2000"""
        book = Book.objects.create(title='Test2', author=self.author, publisher=self.publisher, publication_year=2000)
        book.categories.add(self.category)

        self.assertFalse(book.is_modern())
