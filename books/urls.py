from django.urls import path
from .views import HomeView, BookListView, BookDetailView

app_name = "books"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/<slug:slug>/", BookDetailView.as_view(), name="book_detail"),
]