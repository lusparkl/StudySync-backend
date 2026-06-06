# 📚 StudySync Backend

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-d94e0b?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![OAuth](https://img.shields.io/badge/OAuth_2.0-Bearer-000000?style=for-the-badge)](https://oauth.net/2/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

*Platform to make your studies both enjoyable and effective*

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation)

</div>

---

## ✨ Overview

StudySync is my personal project, intendet to learn how to build real api's and also how to build powerful ai agents, not just chatGPT wrappers. Created for hack club horizons!

###  Key Highlights
-  **JWT Authentication** - Secure token-based user authentication
- **OAuth 2.0 Authentication** - You can use Google/Github account for the authentication!
-  **Workspace Collaboration** - Create shared workspaces to study with your friends
-  **Smart Task & Note Management** - Organize your study plans easily
-  **AI Integration** - Create study plan with ai, it searches for the resources and best way to learn any topic!
-  **Profile Management** - Upload and manage user profile pictures with S3 storage
-  **Production Ready** - You can deploy it to the heroku with few clicks!

---

##  Features

###  Authentication & Authorization
- [x] User registration and login with JWT tokens
- [x] Secure password hashing with Argon2
- [x] Token-based API authorization
- [x] User profile management and editing
- [x] Auth with external services(Google, Github)

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

###  Interactive API Docs
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

👉 **Full API documentation**: See [API.md](API.md)

---

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
### How to contribute

I'll be really happy if you want to contribute to the project. Crete pull requests with detailed descriptoin of what you added and after testing it I'll definetly merge it! Feel free to add new features or to fix existing ones.

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

### Made with ❤️ 

[⬆ Back to top](#-studysync-backend)

</div>

