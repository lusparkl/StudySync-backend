# StudySync API Documentation

## Base URL

Local:
http://localhost:8000

Production:
https://studysync-1930c1223599.herokuapp.com/

## Authentication

Most endpoints require JWT Bearer token.

Header:
Authorization: Bearer <access_token>

## Auth Flow
1. Register/Login user
2. Save access_token
3. Send token with protected requests

## Endpoints

### Users
- POST /users/
- POST /users/login
- PATCH /users/
- PATCH /users/me/profile_picture
- GET /users/me
- GET /users/{user_id}