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
- POST /users - Create user.
- POST /users/login - Login user.
- PATCH /users - Edit user.
- PATCH /users/me/profile_picture - Set user profile picture.
- GET /users/me - Get personal user information.
- GET /users/{user_id} - Get public user information.

### Workspaces

- POST /workspaces - Create workspace.
- PATCH /workspaces/{workspace_id} - Edit workspace.
- GET /workspaces - Get all user workspaces(owned and shared together).
- GET /workspaces/{workspace_id} - Get some special workspace.
- DELETE /workspaces/{workspace_id} - Delete workspace.

### Invites

- POST /workspaces/{workspace_id}/invites - Create invite link.
- POST /invites/{invite_token} - Accept invite to workspace.

### Tasks

- POST workspaces/{workspace_id}/tasks - Create task.
- PATCH taks/{task_id} - Edit task.
- GET workspaces/{workspace_id}/tasks - Get tasks by workspace.
- GET /tasks/{task_id} - Get some special task.
- DELETE /tasks/{task_id} - Delete task.

### Notes

- POST /tasks/{task_id}/notes - Create note.
- PATCH /notes/{note_id} - Edit note.
- GET /tasks/{task_id}/notes - Get notes by task.
- GET /notes/{note_id} - Get some special note.
- DELETE /notes/{note_id} - Delete note.

---
## POST /users

Creates user and returns you already working jwt token.

### Auth

Required: no

### Request body

Content-Type: `application/json`

~~~json
{
  "username": "str",
  "email": "str",
  "password": "str"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "access_token": "str", 
  "token_type": "bearer"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 409 | Conflict | Email/username already exists |
| 422 | Validation Error | Request body has wrong shape or missing fields |
| 500 | Server Error | Unexpected backend error |

### Notes

- You can add some password strength verification on frontend side.
- JWT tocen expires every 10 days

---

## POST users/login

Login already created user. Return you JWT access token.

### Auth

Required: no

### Request body

Content-Type: `application/x-www-form-urlencoded`

~~~json
{
  "username": "str", - it must be named username, but you can put both username or email of the user.
  "password": "str"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "access_token": "str", 
  "token_type": "bearer"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 404 | Not Found | User does not exist |
| 409 | Conflict | Email/username already exists |
| 422 | Validation Error | Request body has wrong shape or missing fields |
| 500 | Server Error | Unexpected backend error |

### Notes

- Make sure that content type is x-www-form-urlencoded.
- We can login user either by email or username.
- JWT tocen expires every 10 days.

---

## PATCH /users

Edit user's email/username.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### Request body

Content-Type: `application/json`

~~~json
{
  "username": "str" | null,
  "email": "str" | null
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "user_id": 0,
  "username": "string",
  "profile_photo_link": "string",
  "email": "string",
  "workspaces": []
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid file type or invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this resource |
| 404 | Not Found | User does not exist |
| 409 | Conflict | Email/username already exists |
| 422 | Validation Error | Request body has wrong shape or missing fields |
| 500 | Server Error | Unexpected backend error |

### Notes

- You can send only username or only email or both.
- Endpoint requires authentication.
- Endpoint returns you already edited user data.

---

## PATCH /users/me/profile_picture

Set user profile picture.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### Request body

Content-Type: `multipart/form-data`

- `file` (required): Image file to upload

### Success response

Status: `200 OK`

~~~json
{
  "user_id": 0,
  "username": "string",
  "profile_photo_link": "string",
  "email": "string",
  "workspaces": []
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid file type |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | User does not exist |
| 422 | Validation Error | File not provided |
| 500 | Server Error | Unexpected backend error |

### Notes

- Only image files are accepted.
- Endpoint requires authentication.

---

## DELETE /users/me/profile_picture

Delete user profile picture.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### Success response

Status: `204 No Content`

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | User does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Removes the profile picture from user account.

---

## GET /users/me

Get personal user information including email and workspaces.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### Success response

Status: `200 OK`

~~~json
{
  "user_id": 0,
  "username": "string",
  "profile_photo_link": "string",
  "email": "string",
  "workspaces": []
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | User does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Returns private user data including email.

---

## GET /users/{user_id}

Get public user information.

### Auth

Required: no

### URL Parameters

- `user_id` (required): User ID

### Success response

Status: `200 OK`

~~~json
{
  "user_id": 0,
  "username": "string",
  "profile_photo_link": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 404 | Not Found | User does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Does not require authentication.
- Returns only public user data without email.

---

## POST /workspaces

Create workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### Request body

Content-Type: `application/json`

~~~json
{
  "title": "str",
  "description": "str | null",
  "deadline": "str (ISO 8601 datetime) | null"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "workspace_id": 0,
  "owner_id": 0,
  "title": "string",
  "description": "string",
  "deadline": "2024-01-01T00:00:00",
  "tasks": [],
  "contributors": []
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 422 | Validation Error | Request body has wrong shape or missing fields |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- User who creates workspace becomes the owner.
- Description and deadline are optional.

---

## PATCH /workspaces/{workspace_id}

Edit workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `workspace_id` (required): Workspace ID

### Request body

Content-Type: `application/json`

~~~json
{
  "title": "str | null",
  "description": "str | null",
  "deadline": "str (ISO 8601 datetime) | null"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "workspace_id": 0,
  "owner_id": 0,
  "title": "string",
  "description": "string",
  "deadline": "2024-01-01T00:00:00",
  "tasks": [],
  "contributors": []
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this workspace |
| 404 | Not Found | Workspace does not exist |
| 422 | Validation Error | Request body has wrong shape |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- You can send only title or only description or only deadline or any combination.
- Only workspace owner can edit workspace.

---

## GET /workspaces

Get all user workspaces (owned and shared together).

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### Success response

Status: `200 OK`

~~~json
[
  {
    "workspace_id": 0,
    "owner_id": 0,
    "title": "string",
    "description": "string",
    "deadline": "2024-01-01T00:00:00",
    "tasks": [],
    "contributors": []
  }
]
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Returns both owned and shared workspaces.

---

## GET /workspaces/{workspace_id}

Get some special workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `workspace_id` (required): Workspace ID

### Success response

Status: `200 OK`

~~~json
{
  "workspace_id": 0,
  "owner_id": 0,
  "title": "string",
  "description": "string",
  "deadline": "2024-01-01T00:00:00",
  "tasks": [],
  "contributors": []
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this workspace |
| 404 | Not Found | Workspace does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Returns workspace with all tasks and contributors.

---

## DELETE /workspaces/{workspace_id}

Delete workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `workspace_id` (required): Workspace ID

### Success response

Status: `204 No Content`

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this workspace |
| 404 | Not Found | Workspace does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Only workspace owner can delete workspace.

---

## POST /workspaces/{workspace_id}/tasks

Create task.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `workspace_id` (required): Workspace ID

### Request body

Content-Type: `application/json`

~~~json
{
  "title": "str",
  "text": "str | null"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "task_id": 0,
  "owner_id": 0,
  "workspace_id": 0,
  "title": "string",
  "text": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this workspace |
| 404 | Not Found | Workspace does not exist |
| 422 | Validation Error | Request body has wrong shape or missing fields |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Text is optional.
- User who creates task becomes the owner.

---

## PATCH /tasks/{task_id}

Edit task.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `task_id` (required): Task ID

### Request body

Content-Type: `application/json`

~~~json
{
  "title": "str | null",
  "text": "str | null"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "task_id": 0,
  "owner_id": 0,
  "workspace_id": 0,
  "title": "string",
  "text": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this task |
| 404 | Not Found | Task does not exist |
| 422 | Validation Error | Request body has wrong shape |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- You can send only title or only text or both.
- Only task owner can edit task.

---

## GET /workspaces/{workspace_id}/tasks

Get tasks by workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `workspace_id` (required): Workspace ID

### Success response

Status: `200 OK`

~~~json
[
  {
    "task_id": 0,
    "owner_id": 0,
    "workspace_id": 0,
    "title": "string",
    "text": "string"
  }
]
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this workspace |
| 404 | Not Found | Workspace does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Returns all tasks in the workspace.

---

## GET /tasks/{task_id}

Get some special task.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `task_id` (required): Task ID

### Success response

Status: `200 OK`

~~~json
{
  "task_id": 0,
  "owner_id": 0,
  "workspace_id": 0,
  "title": "string",
  "text": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this task |
| 404 | Not Found | Task does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.

---

## DELETE /tasks/{task_id}

Delete task.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `task_id` (required): Task ID

### Success response

Status: `204 No Content`

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this task |
| 404 | Not Found | Task does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Only task owner can delete task.

---

## POST /tasks/{task_id}/notes

Create note.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `task_id` (required): Task ID

### Request body

Content-Type: `application/json`

~~~json
{
  "title": "str",
  "text": "str | null"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "note_id": 0,
  "owner_id": 0,
  "task_id": 0,
  "title": "string",
  "text": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this task |
| 404 | Not Found | Task does not exist |
| 422 | Validation Error | Request body has wrong shape or missing fields |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Text is optional.
- User who creates note becomes the owner.

---

## PATCH /notes/{note_id}

Edit note.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `note_id` (required): Note ID

### Request body

Content-Type: `application/json`

~~~json
{
  "title": "str | null",
  "text": "str | null"
}
~~~

### Success response

Status: `200 OK`

~~~json
{
  "note_id": 0,
  "owner_id": 0,
  "task_id": 0,
  "title": "string",
  "text": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid business input |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this note |
| 404 | Not Found | Note does not exist |
| 422 | Validation Error | Request body has wrong shape |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- You can send only title or only text or both.
- Only note owner can edit note.

---

## GET /tasks/{task_id}/notes

Get notes by task.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `task_id` (required): Task ID

### Success response

Status: `200 OK`

~~~json
[
  {
    "note_id": 0,
    "owner_id": 0,
    "task_id": 0,
    "title": "string",
    "text": "string"
  }
]
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this task |
| 404 | Not Found | Task does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Returns all notes for the task.

---

## GET /notes/{note_id}

Get some special note.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `note_id` (required): Note ID

### Success response

Status: `200 OK`

~~~json
{
  "note_id": 0,
  "owner_id": 0,
  "task_id": 0,
  "title": "string",
  "text": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this note |
| 404 | Not Found | Note does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.

---

## DELETE /notes/{note_id}

Delete note.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `note_id` (required): Note ID

### Success response

Status: `204 No Content`

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this note |
| 404 | Not Found | Note does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Only note owner can delete note.

---

## POST /workspaces/{workspace_id}/invites

Create invite link for workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `workspace_id` (required): Workspace ID

### Success response

Status: `200 OK`

~~~json
{
  "invite_link": "string"
}
~~~

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User does not have access to this workspace |
| 404 | Not Found | Workspace does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Only workspace owner can create invite links.
- Invite link does not expire.

---

## POST /invites/{invite_token}

Accept invite to workspace.

### Auth

Required: yes

Header:

~~~http
Authorization: Bearer <access_token>
~~~

### URL Parameters

- `invite_token` (required): Invite token from invite link

### Success response

Status: `200 OK`

No response body

### Error responses

| Status code | Meaning | Example reason |
|---:|---|---|
| 400 | Bad Request | Invalid or expired invite token |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Workspace does not exist |
| 500 | Server Error | Unexpected backend error |

### Notes

- Endpoint requires authentication.
- Adds user as contributor to workspace if not already member.


