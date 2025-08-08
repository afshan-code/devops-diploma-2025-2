# cct-devops-diploma-2025-template

## Book Catalog API

This project provides a simple RESTful API for managing a catalog of books, built with Django and Django REST Framework. It includes a CI/CD pipeline using GitHub Actions for automated testing and Docker image building, and it's set up for deployment to Kubernetes using Helm.

---

## Project Overview 📚

The Book Catalog API allows users to perform standard CRUD (Create, Read, Update, Delete) operations on book records. Each book has the following attributes:

- Title
- Author
- ISBN
- Published date

**Key Features:**

- RESTful Endpoints for CRUD operations  
- Data validation to ensure integrity  
- Health check endpoint for monitoring  

---

## API Usage Examples

All API endpoints are prefixed with `/api/`. For example, running locally on port 8000, the base URL is `http://127.0.0.1:8000/api/`.

1. Get All Books (List)  
Retrieve a list of all books:  
GET /api/books/`

Example Response (200 OK): 
[
  {
    "id": 1,
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "9781234567897",
    "published_date": "2023-01-01",
    "created_at": "2023-01-01T12:00:00Z"
  }
]

2. Create a New Book
Add a new book:
POST /api/books/
Content-Type: application/json

Request body:
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "published_date": "1925-04-10"
}

3. Get a Single Book (Detail)
Retrieve details for a book by ID:
GET /api/books/{id}/

Example Response (200 OK):
{
  "id": 1,
  "title": "Test Book",
  "author": "Test Author",
  "isbn": "9781234567897",
  "published_date": "2023-01-01",
  "created_at": "2023-01-01T12:00:00Z"
}

4. Update an Existing Book
Update book details by ID:
PUT /api/books/{id}/
Content-Type: application/json

Request body:
{
  "title": "The Great Gatsby (Revised)",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "published_date": "1925-04-10"
}
Example Response (200 OK): Returns updated book object.

5. Delete a Book
Remove a book by ID:
DELETE /api/books/{id}/

Example Response (204 No Content): No content returned.

6. Health Check
Check API health status:
GET /api/health/

Example Response (200 OK):
{
  "status": "ok"
}

## Local Build and Run Instructions
Clone the repository:
git clone <your-repository-url>
cd <your-repository-directory>

Create and activate Python virtual environment:
python3 -m venv .venv
source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Apply migrations:
python3 manage.py makemigrations api
python3 manage.py migrate

Run the development server:
python3 manage.py runserver 8000
or use another port if needed
python3 manage.py runserver 8001
Access the API at:
http://127.0.0.1:8000/api/

## CI/CD Pipeline Explanation (GitHub Actions)
Trigger: On push to main or pull requests.

Install Dependencies: Sets up Python and installs requirements.

Run Tests:

Check migrations.

Run tests with pytest.

Docker Build & Push (on main branch):

Build Docker image tagged with commit SHA/version.

Push to container registry (GitHub Container Registry/Docker Hub).

Helm Chart Update (GitOps):

Update values.yaml with new Docker image tag.

Commit and push back to Git repo.

GitOps tool (e.g., ArgoCD) detects change and deploys to Kubernetes.
