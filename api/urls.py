from django.urls import re_path, include
from .views import book_view, health_view, test_view

app_name = 'api'

urlpatterns = [
    re_path(
        r"^$", health_view, name='health'
    ),
    re_path(
        r"^test/", test_view, name='test'
    ),
    re_path(
        r"^books/", book_view, name='books'
    )
]


