# 📚 StudySync Backend

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-d94e0b?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

*A powerful, AI-enhanced collaborative learning platform backend*

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation)

</div>

---

## ✨ Overview

StudySync is my personal project, intendet to learn how to build real api's and also how to build powerful ai agents, not just chatGPT wrappers. Created for hack club horizons btw!

### 🎯 Key Highlights
-  **JWT Authentication** - Secure token-based user authentication
-  **Workspace Collaboration** - Create shared workspaces with invite-based access
-  **Smart Task & Note Management** - Organize your study materials hierarchically
-  **AI Integration** - Create study plan with ai, it searches for the resources and best way to learn any topic!
-  **Profile Management** - Upload and manage user profile pictures with S3 storage
-  **Production Ready** - Deployed on Heroku with PostgreSQL backend

---

## 🎯 Features

### 🔑 Authentication & Authorization
- [x] User registration and login with JWT tokens
- [x] Secure password hashing with Argon2
- [x] Token-based API authorization
- [x] User profile management and editing

### 🛠️ Workspace Management
- [x] Create and manage multiple workspaces
- [x] Invite-based collaboration system
- [x] Share workspaces with team members
- [x] Full CRUD operations on workspaces

### 📋 Task & Note System
- [x] Hierarchical task organization
- [x] Attach multiple notes to tasks
- [x] Edit and delete tasks/notes
- [x] Workspace-based task filtering

### 🧠 AI-Powered Search
- [x] **YouTube Search** - Find educational videos
- [x] **Web Search** - Search across the internet
- [x] **Book Search** - Search and extract PDF content
- [ ] **AI Study Planning** - Still working on this one

### 📸 Storage & Media
- [x] AWS S3 integration for profile photos
- [x] Secure file upload management
- [x] Optimized media storage utilities

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/StudySync-backend.git
cd StudySync-backend
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration:
# - DATABASE_URL
# - AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY
# - API keys for AI services (Exa, OpenAI)
# - Google API key (with services YoutubeDataV3 and Google Books)
```

5. **Initialize database**
```bash
# Run migrations (if using Alembic)
# sqlalchemy init (or your migration tool)
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📖 API Documentation

###  Base URLs
- **Local Development**: `http://localhost:8000`
- **Production**: `https://studysync-1930c1223599.herokuapp.com/`

###  Interactive API Docs
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

###  Authentication
Most endpoints require JWT Bearer token authentication:

```
Header: Authorization: Bearer <access_token>
```

###  Available Endpoints

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| **Users** | POST | `/users` | Create new user |
| | POST | `/users/login` | Login user |
| | PATCH | `/users` | Update user profile |
| | PATCH | `/users/me/profile_picture` | Upload profile picture |
| | GET | `/users/me` | Get current user info |
| | GET | `/users/{user_id}` | Get public user info |
| **Workspaces** | POST | `/workspaces` | Create workspace |
| | PATCH | `/workspaces/{workspace_id}` | Update workspace |
| | GET | `/workspaces` | List user workspaces |
| | GET | `/workspaces/{workspace_id}` | Get workspace details |
| | DELETE | `/workspaces/{workspace_id}` | Delete workspace |
| **Invites** | POST | `/workspaces/{workspace_id}/invites` | Create invite |
| | POST | `/invites/{invite_token}` | Accept invite |
| **Tasks** | POST | `/workspaces/{workspace_id}/tasks` | Create task |
| | PATCH | `/tasks/{task_id}` | Update task |
| | GET | `/workspaces/{workspace_id}/tasks` | List tasks |
| | GET | `/tasks/{task_id}` | Get task details |
| | DELETE | `/tasks/{task_id}` | Delete task |
| **Notes** | POST | `/tasks/{task_id}/notes` | Create note |
| | PATCH | `/notes/{note_id}` | Update note |
| | GET | `/tasks/{task_id}/notes` | List notes |
| | GET | `/notes/{note_id}` | Get note details |
| | DELETE | `/notes/{note_id}` | Delete note |

👉 **Full API documentation**: See [API.md](API.md)

---

## 🏗️ Architecture

### Project Structure
```
StudySync-backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── ai/                  # AI search modules
│   │   ├── search_books.py
│   │   ├── search_web.py
│   │   └── search_youtube.py
│   ├── auth/                # Authentication logic
│   │   ├── authentication.py
│   │   ├── helpers.py
│   │   └── invites.py
│   ├── repositories/        # Data access layer
│   │   ├── notes.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   └── workspaces.py
│   ├── routers/             # API route handlers
│   │   ├── note.py
│   │   ├── task.py
│   │   ├── user.py
│   │   └── workspace.py
│   ├── services/            # Business logic layer
│   │   ├── notes.py
│   │   ├── tasks.py
│   │   ├── user.py
│   │   └── workspaces.py
│   └── storage/             # File storage utilities
│       ├── profile_photos.py
│       └── utils.py
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### Technology Stack
- **Framework**: FastAPI - Modern, fast web framework for building APIs
- **Database**: PostgreSQL - Reliable relational database
- **ORM**: SQLAlchemy - Powerful Python SQL toolkit
- **Authentication**: PyJWT - JSON Web Token implementation
- **Password Security**: pwdlib with Argon2 - Industry-standard password hashing
- **AI/ML**: LangChain + LangGraph - For building AI-powered search
- **Cloud Storage**: AWS S3 - For profile photo storage
- **Search API**: Exa - Advanced search capabilities
- **Server**: Uvicorn - Fast ASGI server
- **File Processing**: PyMuPDF4LLM - PDF extraction and processing

---

## 🧪 Testing

Run the test suite:
```bash
pytest                                  # Run all tests
pytest tests/test_users.py             # Run specific test file
pytest tests/test_notes.py -v          # Verbose output
pytest --cov=app                       # With coverage
```

Current test coverage includes:
- ✅ User authentication and management
- ✅ Workspace operations
- ✅ Task management
- ✅ Note operations
- ✅ AI search capabilities (YouTube, web, books)

---

## 🌟 Usage Examples

### Register & Login
```python
import requests

# Register
response = requests.post('http://localhost:8000/users', json={
    'username': 'john_doe',
    'email': 'john@example.com',
    'password': 'secure_password'
})
token = response.json()['access_token']

# Use token for subsequent requests
headers = {'Authorization': f'Bearer {token}'}
```

### Create Workspace
```python
workspace = requests.post(
    'http://localhost:8000/workspaces',
    json={'name': 'Python Study Group'},
    headers=headers
).json()
```

### Create Task & Notes
```python
task = requests.post(
    f'http://localhost:8000/workspaces/{workspace["id"]}/tasks',
    json={'title': 'Learn FastAPI', 'description': 'Complete the official tutorial'},
    headers=headers
).json()

note = requests.post(
    f'http://localhost:8000/tasks/{task["id"]}/notes',
    json={'content': 'Watched first 3 chapters'},
    headers=headers
).json()
```

---

## 🔌 Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/studysync

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET_NAME=studysync-uploads

# JWT
JWT_SECRET_KEY=your_super_secret_key_here
JWT_ALGORITHM=HS256

# LangChain
LANGCHAIN_API_KEY=your_langchain_key
EXA_API_KEY=your_exa_key

# Environment
ENVIRONMENT=development  # or production
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### Made with ❤️ by a passionate developer

[⬆ Back to top](#-studysync-backend)

</div>

