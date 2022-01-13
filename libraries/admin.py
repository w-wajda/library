from django.contrib import admin
from libraries.models import (
    Author,
    Category,
    Publisher,
    Book,
    Review,
    BorrowedBook
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Author's data", {
            'fields': ('name', 'surname')
        }),
        ('Additional info', {
            'fields': ('date_birth',)
        }),
    )
    search_fields = ('name', 'surname')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Publisher data", {
            'fields': ('name', )
        }),
    )
    search_fields = ('books__title', 'name',)
    list_filter = ('books',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Category data", {
            'fields': ('name',)
        }),
    )
    search_fields = ('books__title', 'name')
    list_filter = ('books', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic data', {
            'fields': ('title', 'author', 'description')
        }),
        ('Additional info', {
            'fields': ('categories', ('publisher', 'publication_year'), 'book_cover')
        }),
    )
    list_display = ('title', 'author', 'publisher', 'publication_year')
    search_fields = ('title', 'author__name', 'author__surname', 'publisher__name')
    list_filter = ('author', 'categories', 'publisher')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Review data", {
            'fields': ('book',)
        }),
        ('Additional info', {
            'fields': ('rating', 'entry')
        }),
    )
    list_display = ('book', 'rating', 'date_review')
    list_filter = ('book', 'rating', 'date_review')
    search_fields = ('book__title',)


@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'date_start', 'date_end')
    search_fields = ('book__title', 'user__first_name', 'user__last_name')
    list_filter = ('date_start', 'date_end')
    list_display = ('book', 'date_start', 'date_end')


