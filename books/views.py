from django.views.generic import ListView, DetailView, TemplateView
from .models import Book


class HomeView(TemplateView):
    template_name = "books/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_books"] = Book.objects.filter(stock__gt=0).order_by("-created_at")[:8]
        return context


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 12

    def get_queryset(self):
        return Book.objects.select_related("category").prefetch_related("authors").order_by("-created_at")


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Book.objects.select_related("category").prefetch_related("authors")