from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from api.models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a sample book for tests that need an existing object
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="978-0-123456-78-9",
            published_date=date(2023, 1, 1)
        )
        self.book_list_url = reverse('books-list')
        self.book_detail_url = reverse('books-detail', args=[self.book.pk])

    def test_create_book(self):
        """Test that a book can be created via POST request."""
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "978-1-234567-89-0",
            "published_date": "2024-05-15"
        }
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(isbn="978-1-234567-89-0").title, "New Book")

    def test_get_book_list(self):
        """Test that the book list is returned correctly."""
        response = self.client.get(self.book_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book.title)

    def test_update_book(self):
        """Test that a book can be updated via PUT request."""
        updated_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "isbn": self.book.isbn,
            "published_date": self.book.published_date
        }
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

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