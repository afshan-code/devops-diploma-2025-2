# cct-devops-diploma-2025-template
Book Catalog APIThis project provides a simple RESTful API for managing a catalog of books, built with Django and Django REST Framework. It includes a CI/CD pipeline using GitHub Actions for automated testing and Docker image building, and it's set up for deployment to Kubernetes using Helm.Project Overview 📚The Book Catalog API allows users to perform standard CRUD (Create, Read, Update, Delete) operations on book records. Each book has a title, author, ISBN, and published date.Key Features:RESTful Endpoints: Standard API endpoints for GET, POST, PUT, and DELETE operations.Data Validation: Ensures data integrity for book records.Health Check: A dedicated endpoint to monitor the application's health.API Usage Examples All API endpoints are prefixed with /api/. For instance, if running locally on port 8000, the base URL is http://127.0.0.1:8000/api/.1. Get All Books (List)Retrieve a list of all books in the catalog.GET /api/books/
Example Response (HTTP 200 OK):[
    {
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "9781234567897",
        "published_date": "2023-01-01",
        "created_at": "2023-01-01T12:00:00Z"
    }
]
2. Create a New BookAdd a new book to the catalog.POST /api/books/
Content-Type: application/json

{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "published_date": "1925-04-10"
}
Example Response (HTTP 201 Created):{
    "id": 2,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "published_date": "1925-04-10",
    "created_at": "2024-01-01T10:30:00Z"
}
3. Get a Single Book (Detail)Retrieve details for a specific book by its ID.GET /api/books/{id}/
Example Response (HTTP 200 OK):{
    "id": 1,
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "9781234567897",
    "published_date": "2023-01-01",
    "created_at": "2023-01-01T12:00:00Z"
}
4. Update an Existing BookUpdate the details of an existing book by its ID.PUT /api/books/{id}/
Content-Type: application/json

{
    "title": "The Great Gatsby (Revised)",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "published_date": "1925-04-10"
}
Example Response (HTTP 200 OK):(Returns the updated book object)5. Delete a BookRemove a book from the catalog by its ID.DELETE /api/books/{id}/
Example Response (HTTP 204 No Content):(No content is returned for a successful deletion)6. Health CheckCheck the health status of the API.GET /api/health/
Example Response (HTTP 200 OK):{
    "status": "ok"
}
Local Build and Run Instructions To run the project locally, follow these steps:Clone the Repository:git clone <your-repository-url>
cd <your-repository-directory>
Create and Activate a Python Virtual Environment:It's highly recommended to use a virtual environment to manage project dependencies.python3 -m venv .venv
source .venv/bin/activate
Install Dependencies:Install all required Python packages using pip.pip install -r requirements.txt

Apply Database Migrations:Apply the necessary database schema changes.python3 manage.py makemigrations api
python3 manage.py migrate
Collect Static Files:Collect all static files into the STATIC_ROOT directory.python3 manage.py collectstatic
When prompted, type yes and press Enter.Run the Development Server:Start the Django development server. If port 8000 is in use, you can specify an alternative, e.g., 8001.python3 manage.py runserver 8000
# or
python3 manage.py runserver 8001
Access the API:Open your web browser and navigate to http://127.0.0.1:8000/api/ (or your chosen port) to see the browsable API.CI/CD Pipeline Explanation (GitHub Actions) 自动化 🚀This project uses GitHub Actions to automate the testing and Docker image building process.The CI/CD pipeline is defined in .github/workflows/main.yml (or similar). It typically includes the following stages:Pull Request / Push to main Trigger:The workflow is triggered on every push to the main branch or on pull requests.Install Dependencies:A custom action (.github/actions/install-dependencies) is used to set up Python and install project dependencies from requirements.txt.Run Tests:Migrations Check: Ensures there are no pending migrations.Pytest: Runs the unit and integration tests defined in api/tests/test_views.py. This step also applies migrations before running tests to ensure a consistent test environment.Docker Build and Push (on main branch push):If tests pass and the commit is on the main branch, a Docker image of the application is built.The image is tagged with the commit SHA or a semantic version.The Docker image is then pushed to a container registry (e.g., GitHub Container Registry, Docker Hub).Helm Chart Update (GitOps Integration):After the Docker image is pushed, the CI/CD pipeline updates the values.yaml file within the books-catalog-chart/ directory to reflect the new Docker image tag.This change is then committed back to the main branch of the Git repository.This Git commit (the update to values.yaml) serves as the trigger for the GitOps tool (e.g., ArgoCD) to detect a change in the desired state and initiate deployment to the Kubernetes cluster.Kubernetes and Helm Setup Instructions ☸️This project is designed for deployment to Kubernetes using Helm.Helm Chart StructureThe Helm chart for this application is located in the books-catalog-chart/ directory and typically includes:Chart.yaml: Defines the chart's metadata (name, version, etc.).values.yaml: Contains default configuration values that can be overridden during deployment. This file is updated by the CI/CD pipeline with the latest Docker image tag.templates/: Contains Kubernetes manifest templates (deployment.yaml, service.yaml, ingress.yaml, etc.) that use values from values.yaml to render the final YAML.Deployment Process (GitOps Flow)Local Development & Push: Developers make changes to the application code, commit, and push to the Git repository.CI/CD Pipeline Execution:GitHub Actions runs tests.On successful tests, a new Docker image is built and pushed to the container registry.The values.yaml in the Helm chart is automatically updated with the new image tag and pushed back to Git.ArgoCD (or similar GitOps Tool) Sync:ArgoCD continuously monitors the Git repository (specifically the main branch of the Helm chart).It detects the new commit to values.yaml.ArgoCD then pulls the updated Helm chart, renders the Kubernetes manifests with the new image tag, and applies them to the target Kubernetes cluster.This ensures that the deployed application always reflects the state defined in Git.Local Kubernetes Deployment (for testing)To deploy to a local Kubernetes cluster (like Minikube or Kind):Ensure Kubernetes Cluster is Running:minikube start
# or
kind create cluster
Build and Push Docker Image to Local Cluster's Docker Daemon:If using Minikube/Kind, configure your Docker client to use the cluster's Docker daemon.eval $(minikube docker-env)
# or for Kind
# docker build -t your-image:tag .
# kind load docker-image your-image:tag
Then build your application's Docker image:docker build -t book-catalog-api:latest .
Install the Helm Chart:Navigate to the root of your project where books-catalog-chart/ is located.helm upgrade --install book-catalog ./books-catalog-chart \
  --set image.tag=latest \
  --wait
book-catalog: The name of your Helm release../books-catalog-chart: Path to your Helm chart.--set image.tag=latest: Overrides the image tag in values.yaml for local testing. In a real CI/CD, this would be handled by the pipeline updating values.yaml.--wait: Waits for all resources to be deployed and ready.Access the Deployed Application:You can get the service URL (if using a NodePort or LoadBalancer service) or configure ingress.minikube service book-catalog-api
This will open the service URL in your browser.
