# Project Management API

This is a Project Management API built with Django and Django Rest Framework (DRF), designed to manage projects, tasks, and user assignments. The API is fully documented with Swagger, dockerized for easy deployment, and utilizes a PostgreSQL database hosted on Supabase.

## Features

- User authentication (JWT-based)
- Project management (CRUD operations)
- Task management within projects
- User roles (Admin, User)
- Task assignment and progress tracking
- Swagger documentation for API endpoints
- Dockerized for seamless development and production setup
- PostgreSQL database hosted on Supabase

## Technologies Used

- **Backend Framework**: Django & Django Rest Framework
- **Database**: PostgreSQL (hosted on Supabase)
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker & Docker Compose
- **Authentication**: JSON Web Tokens (JWT)
- **Hosting/Database**: Supabase (PostgreSQL), Render (Dockerized API)
  
## Installation

To run this project locally, follow these steps:

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A Supabase account with PostgreSQL database setup.
- Python 3.x installed.

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Burger-karl/PMProject.git
   cd PMProject


docker-compose up --build

### DATABASE SETUP

docker-compose exec web python manage.py migrate


### API DOCUMENTATION

http://localhost:8000/swagger/


### RUNNING TESTS

docker-compose exec web python manage.py users.RegisterViewTestCase


### FOR PRODUCTION

docker-compose -f docker-compose.prod.yml up --build
