import { clearStoredToken, getStoredToken } from '../auth/token'

export type TokenResponse = {
  access_token: string
  token_type: string
}

export type UserPublic = {
  user_id: number
  username: string
  profile_photo_link: string | null
}

export type UserPrivate = UserPublic & {
  email: string
  workspaces: Workspace[]
}

export type Workspace = {
  workspace_id: number
  owner_id: number
  title: string
  description: string | null
  deadline: string | null
  tasks: Task[]
  contributors: UserPublic[]
}

export type Task = {
  task_id: number
  owner_id: number
  workspace_id: number
  title: string
  text: string | null
}

export type Note = {
  note_id: number
  owner_id: number
  task_id: number
  title: string
  text: string | null
}

export type ApiErrorBody = {
  detail?: unknown
}

export class ApiError extends Error {
  status: number
  detail: unknown

  constructor(status: number, message: string, detail?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ??
  'http://localhost:8000'

type RequestOptions = {
  method?: 'GET' | 'POST' | 'PATCH' | 'DELETE'
  body?: Record<string, unknown> | URLSearchParams | FormData
  auth?: boolean
}

function errorMessage(status: number, detail: unknown) {
  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'object' && item !== null && 'msg' in item) {
          return String(item.msg)
        }

        return 'Validation error'
      })
      .join(', ')
  }

  if (status === 401) return 'Your session expired. Please log in again.'
  if (status === 403) return 'You do not have access to this resource.'
  if (status === 404) return 'This item was not found.'

  return 'Something went wrong. Please try again.'
}

async function parseError(response: Response) {
  const text = await response.text()

  if (!text) {
    throw new ApiError(response.status, errorMessage(response.status, undefined))
  }

  try {
    const data = JSON.parse(text) as ApiErrorBody
    throw new ApiError(
      response.status,
      errorMessage(response.status, data.detail),
      data.detail,
    )
  } catch (error) {
    if (error instanceof ApiError) throw error
    throw new ApiError(response.status, errorMessage(response.status, text), text)
  }
}

async function apiRequest<T>(path: string, options: RequestOptions = {}) {
  const headers = new Headers()
  const method = options.method ?? 'GET'
  const shouldAuth = options.auth ?? true
  const token = getStoredToken()

  if (shouldAuth && token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  let body: BodyInit | undefined

  if (options.body instanceof URLSearchParams) {
    headers.set('Content-Type', 'application/x-www-form-urlencoded')
    body = options.body
  } else if (options.body instanceof FormData) {
    body = options.body
  } else if (options.body) {
    headers.set('Content-Type', 'application/json')
    body = JSON.stringify(options.body)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body,
  })

  if (response.status === 401) {
    clearStoredToken()
    window.dispatchEvent(new Event('studysync:unauthorized'))
  }

  if (!response.ok) {
    await parseError(response)
  }

  if (response.status === 204) {
    return undefined as T
  }

  const text = await response.text()
  return (text ? JSON.parse(text) : undefined) as T
}

export function apiErrorToMessage(error: unknown) {
  if (error instanceof ApiError) return error.message
  if (error instanceof Error) return error.message
  return 'Something went wrong. Please try again.'
}

export function getApiBaseUrl() {
  return API_BASE_URL
}

export const api = {
  register(payload: { username: string; email: string; password: string }) {
    return apiRequest<TokenResponse>('/users/', {
      method: 'POST',
      auth: false,
      body: payload,
    })
  },
  login(identifier: string, password: string) {
    const body = new URLSearchParams()
    body.set('username', identifier)
    body.set('password', password)

    return apiRequest<TokenResponse>('/login/', {
      method: 'POST',
      auth: false,
      body,
    })
  },
  getMe() {
    return apiRequest<UserPrivate>('/users/me')
  },
  getUser(userId: number) {
    return apiRequest<UserPublic>(`/users/${userId}`)
  },
  updateMe(payload: { username?: string; email?: string }) {
    return apiRequest<UserPrivate>('/users/', {
      method: 'PATCH',
      body: payload,
    })
  },
  changePassword(payload: { old_password: string; new_password: string }) {
    return apiRequest<UserPrivate>('/users/me/password', {
      method: 'PATCH',
      body: payload,
    })
  },
  updateProfilePicture(file: File) {
    const body = new FormData()
    body.set('file', file)

    return apiRequest<UserPrivate>('/users/me/profile_picture', {
      method: 'PATCH',
      body,
    })
  },
  deleteProfilePicture() {
    return apiRequest<UserPrivate>('/users/me/profile_picture', {
      method: 'DELETE',
    })
  },
  getWorkspaces() {
    return apiRequest<Workspace[]>('/workspaces')
  },
  getWorkspace(workspaceId: number) {
    return apiRequest<Workspace>(`/workspaces/${workspaceId}`)
  },
  createWorkspace(payload: {
    title: string
    description?: string | null
    deadline?: string | null
  }) {
    return apiRequest<Workspace>('/workspaces', {
      method: 'POST',
      body: payload,
    })
  },
  updateWorkspace(
    workspaceId: number,
    payload: {
      title?: string | null
      description?: string | null
      deadline?: string | null
    },
  ) {
    return apiRequest<Workspace>(`/workspaces/${workspaceId}`, {
      method: 'PATCH',
      body: payload,
    })
  },
  deleteWorkspace(workspaceId: number) {
    return apiRequest<void>(`/workspaces/${workspaceId}`, {
      method: 'DELETE',
    })
  },
  createInvite(workspaceId: number) {
    return apiRequest<{ invite_link: string }>(`/workspaces/${workspaceId}/invites`, {
      method: 'POST',
    })
  },
  acceptInvite(inviteToken: string) {
    return apiRequest<void>(`/invites/${encodeURIComponent(inviteToken)}`, {
      method: 'POST',
    })
  },
  getTasks(workspaceId: number) {
    return apiRequest<Task[]>(`/workspaces/${workspaceId}/tasks`)
  },
  getTask(taskId: number) {
    return apiRequest<Task>(`/tasks/${taskId}`)
  },
  createTask(workspaceId: number, payload: { title: string; text?: string | null }) {
    return apiRequest<Task>(`/workspaces/${workspaceId}/tasks`, {
      method: 'POST',
      body: payload,
    })
  },
  updateTask(taskId: number, payload: { title?: string | null; text?: string | null }) {
    return apiRequest<Task>(`/tasks/${taskId}`, {
      method: 'PATCH',
      body: payload,
    })
  },
  deleteTask(taskId: number) {
    return apiRequest<void>(`/tasks/${taskId}`, {
      method: 'DELETE',
    })
  },
  getNotes(taskId: number) {
    return apiRequest<Note[]>(`/tasks/${taskId}/notes`)
  },
  getNote(noteId: number) {
    return apiRequest<Note>(`/notes/${noteId}`)
  },
  createNote(taskId: number, payload: { title: string; text?: string | null }) {
    return apiRequest<Note>(`/tasks/${taskId}/notes`, {
      method: 'POST',
      body: payload,
    })
  },
  updateNote(noteId: number, payload: { title?: string | null; text?: string | null }) {
    return apiRequest<Note>(`/notes/${noteId}`, {
      method: 'PATCH',
      body: payload,
    })
  },
  deleteNote(noteId: number) {
    return apiRequest<void>(`/notes/${noteId}`, {
      method: 'DELETE',
    })
  },
}
