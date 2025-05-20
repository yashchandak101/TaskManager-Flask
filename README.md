# 🗂️ Task Management REST API

A RESTful API built with Flask and PostgreSQL to manage users, projects, and tasks with support for dependencies and logical constraints.

---

## 📌 Features

- User CRUD (Create, Read)
- Project CRUD (Create, Read)
- Task Management under Projects
- Task Dependency Handling
- Logical constraints on task completion & user deletion
- Input validation (email, status)
- Error handling with appropriate HTTP status codes

---

## 🚀 Technologies Used

- Python 3
- Flask
- PostgreSQL
- SQLAlchemy (ORM)
- PG Admin
- Postman (for API testing)

---

## create and activate venv
- python -m venv venv
- venv\Scripts\activate

## Connect DB (password = password while installing pg admin)
- SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/task_db"

## 🧪 API Testing (Postman)
Use Postman to test the following endpoints:

## 👤 User Endpoints
- POST /api/users

- GET /api/users

- GET /api/users/<user_id>

## 📁 Project Endpoints
- POST /api/projects

- GET /api/projects

- GET /api/projects/<project_id>

- GET /api/projects/<project_id>/tasks

## ✅ Task Endpoints
- POST /api/projects/<project_id>/tasks

- GET /api/tasks/<task_id>

- PUT /api/tasks/<task_id>/status

- GET /api/tasks?assignee_id=<id>

- GET /api/tasks?status=<status>

- POST /api/tasks/<task_id>/dependencies
