from django.contrib import admin
from .models import Category, Author, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "created_at")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "publisher", "category", "price", "stock", "is_available", "published_date", "created_at")
    search_fields = ("title", "authors__first_name", "authors__last_name")
    list_filter = ("category", "authors", "published_date")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("authors",)
    ordering = ("-created_at",)