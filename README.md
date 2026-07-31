# Attendance System v2

This project aims to re-architect and re-implement the attendance system for improved flexibility, reliability, and maintainability. The new architecture adopts a **Clean Architecture** approach for the backend, utilizes **FastAPI** for robust API development, and integrates **Flutter** for a cross-platform mobile application.

## Project Structure

```
attendance-system-v2/
│
├── mobile_app/           # Flutter mobile application
│   ├── lib/
│   │   ├── screens/      # UI screens/pages
│   │   ├── models/       # Data models (e.g., DTOs, entities)
│   │   ├── services/     # Business logic, API calls, local storage
│   │   ├── widgets/      # Reusable UI components
│   │   └── main.dart     # Application entry point
│
├── backend/              # FastAPI backend with Clean Architecture
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   └── v1/   # API versioning
│   │   │   ├── core/     # Core configurations, security, and utilities
│   │   │   │   ├── config/    # Application settings
│   │   │   │   └── security/  # Authentication (JWT) and authorization
│   │   │   ├── db/       # Database interactions
│   │   │   │   ├── migrations/ # Alembic migration scripts
│   │   │   │   └── repositories/ # Data access layer (CRUD operations)
│   │   │   ├── services/ # Business logic and use cases
│   │   │   ├── schemas/  # Pydantic models for request/response validation
│   │   │   └── main.py   # FastAPI application entry point
│   │   ├── tests/        # Unit and integration tests
│   │   └── scripts/      # Utility scripts (e.g., initial data seeding)
│   ├── Dockerfile        # Dockerfile for backend service
│   └── requirements.txt  # Python dependencies
│
├── database/             # Database schema and initial setup
│   └── schema.sql        # SQL schema definition
│
├── .github/              # GitHub Actions CI/CD workflows
│   └── workflows/
│       └── main.yml
│
├── docker-compose.yml    # Docker Compose configuration
│
└── README.md             # Project overview and documentation
```

## Technologies Used

### Backend
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: Python SQL toolkit and Object Relational Mapper (ORM) that gives application developers the full power and flexibility of SQL.
- **Alembic**: Lightweight database migration tool for usage with SQLAlchemy.
- **Pydantic**: Data validation and settings management using Python type hints.
- **JWT (JSON Web Tokens)**: For secure authentication and authorization.
- **Docker**: For containerization, ensuring consistent environments across development, testing, and production.

### Mobile App
- **Flutter**: Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.
- **Provider/Riverpod**: State management solutions for Flutter.
- **Dio**: A powerful HTTP client for Dart, which supports Interceptors, FormData, Request Cancellation, File Downloading, Timeout, etc.
- **SQFlite**: SQLite plugin for Flutter, providing local database capabilities for offline support.

## Architectural Principles

### Clean Architecture (Backend)
- **Separation of Concerns**: Clear boundaries between layers (Presentation, Application Business Rules, Enterprise Business Rules, Infrastructure).
- **Independent of Frameworks**: The architecture does not depend on the existence of some library of feature-laden software.
- **Independent of Database**: The business rules are not bound to the database.
- **Independent of UI**: The UI can change easily, without changing the rest of the system.
- **Testability**: Business rules can be tested without the UI, Database, Web Server, or any other external element.

### Mobile App
- **Offline First**: The application is designed to work effectively without a constant internet connection, leveraging local storage.
- **Modular Design**: Breaking down the application into smaller, manageable modules for better organization and scalability.
- **State Management**: Efficient handling of application state to ensure a responsive and predictable user experience.

## Setup and Installation

This section provides instructions to set up and run the Attendance System locally.

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Flutter SDK

### 1. Clone the Repository

```bash
git clone <repository_url>
cd attendance-system-v2
```

### 2. Database Setup (using Docker Compose)

Navigate to the root of the project and start the database service using Docker Compose:

```bash
docker-compose up -d db
```

This will start a PostgreSQL container and initialize the database with the schema defined in `database/schema.sql`.

### 3. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a Python virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend/` directory with the following content. Ensure `SECRET_KEY` is a strong, randomly generated string.
    ```env
    POSTGRES_SERVER=db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=attendance_db
    SECRET_KEY=YOUR_SUPER_SECRET_KEY_CHANGE_ME
    ACCESS_TOKEN_EXPIRE_MINUTES=10080 # 7 days
    ```
    *Note: When running the backend directly (not via docker-compose), `POSTGRES_SERVER` should be `localhost` if PostgreSQL is running directly on your machine, or the IP address of your PostgreSQL server.* 

5.  **Run Alembic Migrations:**
    Initialize Alembic (if not already done):
    ```bash
    alembic init -t generic src/app/db/migrations
    ```
    *Note: The `env.py` and `alembic.ini` files are already configured for this project.*

    Generate a new migration (if you make changes to models):
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```

    Apply migrations to the database:
    ```bash
    alembic upgrade head
    ```

6.  **Run the FastAPI application:**
    ```bash
    uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend API will be available at `http://localhost:8000`.

### 4. Mobile App Setup

1.  **Navigate to the mobile app directory:**
    ```bash
    cd mobile_app
    ```

2.  **Get Flutter dependencies:**
    ```bash
    flutter pub get
    ```

3.  **Run the Flutter application:**
    ```bash
    flutter run
    ```
    Ensure you have a device or emulator connected and configured for Flutter development.

### 5. Running with Docker Compose (Full Stack)

To run both the database and the backend service using Docker Compose:

1.  **Navigate to the root of the project:**
    ```bash
    cd attendance-system-v2
    ```

2.  **Build and start the services:**
    ```bash
    docker-compose up --build -d
    ```
    This will build the backend Docker image, start the PostgreSQL database, and then start the FastAPI backend. The backend will be accessible at `http://localhost:8000`.

3.  **Stop the services:**
    ```bash
    docker-compose down
    ```

## CI/CD with GitHub Actions

The project includes a basic GitHub Actions workflow (`.github/workflows/main.yml`) that performs the following:
-   **Test Backend**: Runs tests for the FastAPI backend on push and pull requests to the `main` branch.
-   **Build Docker Image**: Builds the Docker image for the backend on push to the `main` branch.

Further steps for deployment (e.g., pushing to a container registry, deploying to a cloud provider) can be added to this workflow.

## Future Enhancements
-   User management and roles.
-   More sophisticated attendance rules (e.g., geofencing).
-   Reporting and analytics features.
-   Push notifications for attendance reminders.
-   Comprehensive unit and integration tests for both backend and mobile app.

---
*Generated by Manus AI*
