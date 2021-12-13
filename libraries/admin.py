from django.contrib import admin
from libraries.models import Author, Category, Publisher, Book


class AuthorAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Author's data", {
            'fields': ('name', 'surname')
        }),
        ('Additional info', {
            'fields': ('date_birth',)
        })
    )
    search_fields = ('name', 'surname')


class PublisherAdmin(admin.ModelAdmin):
    fields = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    search_fields = ('name',)


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
    search_fields = ('title', 'author', 'publisher')
    list_filter = ('author', 'categories', 'publisher')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
