# 🗂️ Task Management REST API

A RESTful API built with Flask and PostgreSQL with JWT Auth to manage users, projects, and tasks with support for dependencies and logical constraints.

---

## 📌 Features

- User CRUD (Create, Read)
- Project CRUD (Create, Read)
- Task Management under Projects
- Task Dependency Handling
- Logical constraints on task completion & user deletion
- Input validation (email, status)
- JWT Auth
- Error handling with appropriate HTTP status codes

---

## 🚀 Technologies Used

- Python 3
- Flask
- PostgreSQL
- JWT Auth
- SQLAlchemy (ORM)
- PG Admin
- Postman (for API testing)

---

## create and activate venv
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt


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

## Endpoint	jwt token
- /login, /users (POST, GET)	❌ No Auth
- Everything else	✅ Auth



![delete user by id fail if task status not comleted](https://github.com/user-attachments/assets/6cb28c4d-16ed-4a7d-b9a3-4ab318ed978c)
![list of task by user id](https://github.com/user-attachments/assets/ca578b46-8e9b-46e3-8024-4d33e8a73234)
![list status](https://github.com/user-attachments/assets/f341d8cf-7a89-4bd8-b216-796cd7393bd1)
![update or patch status](https://github.com/user-attachments/assets/432fa28e-2031-4560-a210-ac4bc2a88078)
![task by task id](https://github.com/user-attachments/assets/2234f669-ffcf-46a4-b26f-19972dc030a6)
![list of tasks by project id](https://github.com/user-attachments/assets/37457b53-c0c4-4fc3-be85-535948e651e1)
![create task](https://github.com/user-attachments/assets/63a3c4e1-962a-44fb-aecf-5eec7a37dc68)
![project by id](https://github.com/user-attachments/assets/2a794468-d575-4579-814e-291de94a5c81)
![List of projects](https://github.com/user-attachments/assets/fbd186d1-d21b-4e33-bfa4-5ebbfd754c2a)
![create project](https://github.com/user-attachments/assets/6c5edc55-9700-4b45-b17c-02aa7a468b3a)
![user by id](https://github.com/user-attachments/assets/f4a559fa-31b6-4705-b86e-baa0a48df9db)
![bearer token](https://github.com/user-attachments/assets/29292415-fc83-45a4-8eb3-75076c260d43)
![List of users](https://github.com/user-attachments/assets/65438979-2765-4e3d-88c5-12e7241bbb22)
![login ](https://github.com/user-attachments/assets/e051d0ac-d513-49cc-ae9a-0f4f22447a22)
![Create user or Signup](https://github.com/user-attachments/assets/24370a2b-94a9-41d2-b395-6c84438e1516)
![create user](https://github.com/user-attachments/assets/c0753263-56aa-44ba-87ff-d7f522bcfa62)



