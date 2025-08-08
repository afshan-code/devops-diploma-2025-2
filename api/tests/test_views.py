# api/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from api.models import Book

# api/tests/test_views.py

# ... other imports
from datetime import date

class BookAPITestCase(APITestCase):

    def setUp(self):
        # ... unchanged code
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="978-0-123456-78-9",
            published_date=date(2023, 1, 1)
        )
        # ... unchanged URL reversing
        self.book_list_url = reverse('api:books-list')
        self.book_detail_url = reverse('api:books-detail', args=[self.book.pk])

    def test_create_book(self):
        # The data for this test is already a string, so no changes are needed here.
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "978-1-234567-89-0",
            "published_date": "2024-05-15"
        }
        # ... rest of the method

    def test_update_book(self):
        """Test that a book can be updated via PUT request."""
        updated_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "isbn": self.book.isbn,
            # Convert date object to a string for the request
            "published_date": str(self.book.published_date)
        }
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    # ... rest of the test methods

    def test_delete_book(self):
        """Test that a book can be deleted via DELETE request."""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

class HealthViewTest(APITestCase):

    def test_health_check_is_correct(self):
        """Test the health check endpoint."""
        url = reverse('api:health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'ok')