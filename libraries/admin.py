from django.contrib import admin
from libraries.models import (
    Author,
    Category,
    Publisher,
    Book,
    Review,
    BorrowedBook
)


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


class PublisherAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Publisher data", {
            'fields': ('name', )
        }),
    )
    search_fields = ('books__title', 'name',)
    list_filter = ('books',)


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Category data", {
            'fields': ('name',)
        }),
    )
    search_fields = ('books__title', 'name')
    list_filter = ('books', )


class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic data', {
            'fields': ('title', 'author', 'description')
        }),
        ('Additional info', {
            'fields': ('categories', ('publisher', 'publication_year'))
        }),
    )
    list_display = ('title', 'author', 'publisher', 'publication_year')
    search_fields = ('title', 'author__name', 'author__surname', 'publisher__name')
    list_filter = ('author', 'categories', 'publisher')


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


class BorrowedBookAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'date_start', 'date_end')
    search_fields = ('book__title', 'user__first_name', 'user__last_name')
    list_filter = ('date_start', 'date_end')
    list_display = ('book', 'date_start', 'date_end')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
