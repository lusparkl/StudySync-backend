import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { differenceInCalendarDays, isValid, parseISO } from 'date-fns'
import {
  ArrowRight,
  CalendarDays,
  Clipboard,
  Hash,
  Link2,
  Plus,
  ShieldCheck,
  Trash2,
  Users,
} from 'lucide-react'
import clsx from 'clsx'
import { toast } from 'sonner'

import { AppIcon } from '../components/AppIcon'
import { Avatar } from '../components/Avatar'
import { EditableText } from '../components/EditableText'
import { EmptyState } from '../components/EmptyState'
import { ErrorView, LoadingView } from '../components/StatusView'
import { api, apiErrorToMessage } from '../lib/api'
import {
  compactDate,
  dateInputToIso,
  dateInputValue,
  normalizeOptional,
} from '../lib/format'
import { numberParam } from '../lib/route'

export function WorkspacePage() {
  const params = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const workspaceId = numberParam(params.workspaceId)

  const workspaceQuery = useQuery({
    queryKey: ['workspace', workspaceId],
    queryFn: () => api.getWorkspace(workspaceId ?? 0),
    enabled: workspaceId !== null,
  })

  const tasksQuery = useQuery({
    queryKey: ['tasks', workspaceId],
    queryFn: () => api.getTasks(workspaceId ?? 0),
    enabled: workspaceId !== null,
  })

  const meQuery = useQuery({
    queryKey: ['me'],
    queryFn: api.getMe,
  })

  const updateWorkspaceMutation = useMutation({
    mutationFn: (payload: {
      title?: string | null
      description?: string | null
      deadline?: string | null
    }) => api.updateWorkspace(workspaceId ?? 0, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspace', workspaceId] })
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const deleteWorkspaceMutation = useMutation({
    mutationFn: () => api.deleteWorkspace(workspaceId ?? 0),
    onSuccess: () => {
      toast.success('Study space deleted')
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
      navigate('/app', { replace: true })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const inviteMutation = useMutation({
    mutationFn: () => api.createInvite(workspaceId ?? 0),
    onSuccess: async (payload) => {
      const link = toFrontendInviteLink(payload.invite_link)
      try {
        await navigator.clipboard.writeText(link)
        toast.success('Invite link copied')
      } catch {
        toast.message('Invite link ready', { description: link })
      }
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  if (workspaceId === null) {
    return (
      <ErrorView
        title="Workspace not found"
        message="The workspace id in this route is not valid."
      />
    )
  }

  if (workspaceQuery.isLoading) {
    return <LoadingView label="Loading workspace" />
  }

  if (workspaceQuery.isError || !workspaceQuery.data) {
    return (
      <ErrorView
        title="Workspace not available"
        message={apiErrorToMessage(workspaceQuery.error)}
      />
    )
  }

  const workspace = workspaceQuery.data
  const tasks = tasksQuery.data ?? []
  const isOwner = meQuery.data?.user_id === workspace.owner_id
  const nextTask = tasks[0] ?? null
  const memberCount = workspace.contributors.length + 1
  const deadlineStatus = getDeadlineStatus(workspace.deadline)

  async function saveWorkspaceTitle(nextTitle: string) {
    if (!nextTitle) {
      toast.error('Workspace title cannot be empty')
      return
    }

    await updateWorkspaceMutation.mutateAsync({ title: nextTitle })
  }

  async function deleteWorkspace() {
    const confirmed = window.confirm(
      `Delete "${workspace.title}" and all of its tasks?`,
    )
    if (!confirmed) return
    deleteWorkspaceMutation.mutate()
  }

  return (
    <article className="page workspace-page">
      <section className="workspace-overview">
        <header className="workspace-hero">
          <div className="page-kicker">
            <span className="workspace-marker large" aria-hidden="true">
              <AppIcon name="study-space" size={26} />
            </span>
            Study space
          </div>
          <EditableText
            value={workspace.title}
            placeholder="Untitled study space"
            title
            variant="document"
            saving={updateWorkspaceMutation.isPending}
            onSave={saveWorkspaceTitle}
          />
          <EditableText
            value={workspace.description ?? ''}
            placeholder="Add a short description for this study space..."
            multiline
            variant="document"
            saving={updateWorkspaceMutation.isPending}
            onSave={(value) =>
              updateWorkspaceMutation.mutateAsync({
                description: normalizeOptional(value),
              })
            }
          />
        </header>

        <aside className="workspace-command-panel" aria-label="Workspace controls">
          <div className={clsx('deadline-pill', deadlineStatus.tone)}>
            <CalendarDays size={16} />
            <span>{deadlineStatus.label}</span>
          </div>
          <label className="deadline-control">
            <span>Due date</span>
            <input
              type="date"
              value={dateInputValue(workspace.deadline)}
              onChange={(event) =>
                updateWorkspaceMutation.mutate({
                  deadline: dateInputToIso(event.target.value),
                })
              }
              aria-label="Workspace deadline"
            />
          </label>
          <div className="workspace-action-grid">
            <button
              type="button"
              className="button button-secondary"
              onClick={() => inviteMutation.mutate()}
              disabled={inviteMutation.isPending}
            >
              <Clipboard size={16} />
              Copy invite
            </button>
            <button
              type="button"
              className="button button-danger"
              onClick={deleteWorkspace}
              disabled={deleteWorkspaceMutation.isPending}
            >
              <Trash2 size={16} />
              Delete
            </button>
          </div>
        </aside>
      </section>

      <section className="workspace-meta-grid" aria-label="Workspace summary">
        <div>
          <span className="meta-label">
            <CalendarDays size={14} />
            Deadline
          </span>
          <strong>{compactDate(workspace.deadline)}</strong>
          <small>{deadlineStatus.detail}</small>
        </div>
        <div>
          <span className="meta-label">
            <AppIcon name="task" size={18} />
            Tasks
          </span>
          <strong>{tasks.length}</strong>
          <small>{tasks.length === 1 ? 'study goal' : 'study goals'}</small>
        </div>
        <div>
          <span className="meta-label">
            <ShieldCheck size={14} />
            Access
          </span>
          <strong>{isOwner ? 'Owner' : 'Shared'}</strong>
          <small>Workspace #{workspace.workspace_id}</small>
        </div>
        <div>
          <span className="meta-label">
            <Users size={14} />
            Members
          </span>
          <strong>{memberCount}</strong>
          <small>{workspace.contributors.length} collaborators</small>
        </div>
      </section>

      <section className="workspace-team-panel" aria-label="Workspace team">
        <div>
          <span className="team-label">
            <Users size={16} />
            Team
          </span>
          <div className="avatar-stack">
            {workspace.contributors.length ? (
              workspace.contributors.map((contributor) => (
                <Avatar
                  key={contributor.user_id}
                  name={contributor.username}
                  src={contributor.profile_photo_link}
                  size="sm"
                />
              ))
            ) : (
              <small>No invited collaborators yet</small>
            )}
          </div>
        </div>
        <button
          type="button"
          className="button button-ghost"
          onClick={() => inviteMutation.mutate()}
          disabled={inviteMutation.isPending}
        >
          <Link2 size={16} />
          Invite people
        </button>
      </section>

      <section className="workspace-focus-grid">
        <div className="workspace-next-panel">
          <p className="eyebrow">Next up</p>
          {nextTask ? (
            <Link
              className="next-task-link"
              to={`/app/workspaces/${workspace.workspace_id}/tasks/${nextTask.task_id}`}
            >
              <span className="task-icon">
                <AppIcon name="task" size={23} />
              </span>
              <span>
                <strong>{nextTask.title}</strong>
                <small>{nextTask.text || 'Open and start collecting notes.'}</small>
              </span>
              <ArrowRight size={16} />
            </Link>
          ) : (
            <p className="panel-muted">Create a first task to start shaping this space.</p>
          )}
        </div>

        <NewTaskComposer workspaceId={workspace.workspace_id} />
      </section>

      <section className="content-section workspace-tasks-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Goals</p>
            <h2>Tasks</h2>
          </div>
          <span className="task-count-chip">{tasks.length}</span>
        </div>

        {tasksQuery.isLoading ? <LoadingView label="Loading tasks" /> : null}

        {tasksQuery.isError ? (
          <ErrorView
            title="Tasks not available"
            message={apiErrorToMessage(tasksQuery.error)}
          />
        ) : null}

        {!tasksQuery.isLoading && !tasksQuery.isError && tasks.length === 0 ? (
          <EmptyState
            icon={<AppIcon name="task" size={34} />}
            title="No tasks yet"
            description="Add a study goal, assignment, reading list, or practice session."
          />
        ) : null}

        <div className="task-list workspace-task-list">
          {!tasksQuery.isError && tasks.map((task) => (
            <Link
              key={task.task_id}
              className="task-card"
              to={`/app/workspaces/${workspace.workspace_id}/tasks/${task.task_id}`}
            >
              <span className="task-icon">
                <AppIcon name="task" size={23} />
              </span>
              <span className="task-card-copy">
                <strong>{task.title}</strong>
                <small>{task.text || 'No task details yet'}</small>
              </span>
              <span className="task-card-meta">
                <Hash size={13} />
                {task.task_id}
              </span>
              <ArrowRight className="task-card-arrow" size={16} />
            </Link>
          ))}
        </div>
      </section>
    </article>
  )
}

function NewTaskComposer({ workspaceId }: { workspaceId: number }) {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [text, setText] = useState('')

  const createTaskMutation = useMutation({
    mutationFn: () =>
      api.createTask(workspaceId, {
        title: title.trim() || 'Untitled task',
        text: normalizeOptional(text),
      }),
    onSuccess: (task) => {
      toast.success('Task created')
      queryClient.invalidateQueries({ queryKey: ['tasks', workspaceId] })
      queryClient.invalidateQueries({ queryKey: ['workspace', workspaceId] })
      setTitle('')
      setText('')
      navigate(`/app/workspaces/${workspaceId}/tasks/${task.task_id}`)
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    createTaskMutation.mutate()
  }

  return (
    <form className="inline-composer task-composer" onSubmit={submit}>
      <div className="task-composer-copy">
        <p className="eyebrow">Quick add</p>
        <strong>New study goal</strong>
      </div>
      <div className="task-composer-fields">
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Task title"
          aria-label="New task title"
        />
        <input
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Optional details, reading, links..."
          aria-label="New task details"
        />
      </div>
      <button
        type="submit"
        className="button button-primary"
        disabled={createTaskMutation.isPending}
      >
        <Plus size={16} />
        Add
      </button>
    </form>
  )
}

function getDeadlineStatus(deadline: string | null) {
  if (!deadline) {
    return {
      label: 'No deadline',
      detail: 'Add one when the study space has a target date.',
      tone: 'neutral',
    }
  }

  const date = parseISO(deadline)
  if (!isValid(date)) {
    return {
      label: 'No deadline',
      detail: 'The saved date could not be read.',
      tone: 'neutral',
    }
  }

  const days = differenceInCalendarDays(date, new Date())

  if (days < 0) {
    return {
      label: `${Math.abs(days)}d overdue`,
      detail: 'Past the saved due date.',
      tone: 'danger',
    }
  }

  if (days === 0) {
    return {
      label: 'Due today',
      detail: 'Today is the saved due date.',
      tone: 'warning',
    }
  }

  if (days <= 7) {
    return {
      label: `${days}d left`,
      detail: 'Coming up soon.',
      tone: 'warning',
    }
  }

  return {
    label: `${days}d left`,
    detail: 'Plenty of time left.',
    tone: 'neutral',
  }
}

function toFrontendInviteLink(rawInvite: string) {
  const origin = window.location.origin

  try {
    const parsed = new URL(rawInvite)
    const token = parsed.pathname.split('/').filter(Boolean).at(-1)
    return token ? `${origin}/invite/${encodeURIComponent(token)}` : rawInvite
  } catch {
    return `${origin}/invite/${encodeURIComponent(rawInvite)}`
  }
}
