from django.urls import path
from .views import RegisterView, BookView, BookDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    # CRUD na mão
    path("books/", BookView.as_view(), name="books"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
]
