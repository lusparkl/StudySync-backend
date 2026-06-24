import { useState } from 'react'
import type { FormEvent } from 'react'
import { NavLink, Outlet, useLocation, useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  CalendarDays,
  ChevronsLeft,
  Moon,
  LogOut,
  Menu,
  Plus,
  Settings,
  Sparkles,
  Sun,
  X,
} from 'lucide-react'
import clsx from 'clsx'
import { toast } from 'sonner'

import { useAuth } from '../auth/useAuth'
import { api, apiErrorToMessage } from '../lib/api'
import { compactDate, dateInputToIso, normalizeOptional } from '../lib/format'
import { useTheme } from '../theme/useTheme'
import { AppIcon } from './AppIcon'
import { Avatar } from './Avatar'
import { BrandLogo } from './BrandLogo'
import { LoadingView } from './StatusView'

export type ShellContext = {
  openCreateWorkspace: () => void
}

export function AppShell() {
  const { logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const location = useLocation()
  const params = useParams()
  const [isCreating, setIsCreating] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const meQuery = useQuery({
    queryKey: ['me'],
    queryFn: api.getMe,
  })

  const workspacesQuery = useQuery({
    queryKey: ['workspaces'],
    queryFn: api.getWorkspaces,
  })

  const activeWorkspaceId = Number(params.workspaceId)
  const workspaces = workspacesQuery.data ?? []
  const sharedCount = workspaces.filter(
    (workspace) => meQuery.data && workspace.owner_id !== meQuery.data.user_id,
  ).length

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  if (meQuery.isLoading) {
    return <LoadingView label="Opening your study space" />
  }

  return (
    <div className="app-shell">
      <button
        type="button"
        className="mobile-menu-button icon-button"
        aria-label="Open sidebar"
        title="Open sidebar"
        onClick={() => setSidebarOpen(true)}
      >
        <Menu size={18} />
      </button>

      <aside className={clsx('sidebar', sidebarOpen && 'sidebar-open')}>
        <div className="sidebar-top">
          <NavLink className="brand" to="/app" onClick={() => setSidebarOpen(false)}>
            <BrandLogo />
            <span>StudySync</span>
          </NavLink>
          <button
            type="button"
            className="icon-button sidebar-close"
            aria-label="Close sidebar"
            title="Close sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={16} />
          </button>
        </div>

        {meQuery.data ? (
          <NavLink
            className="user-chip"
            to="/settings"
            onClick={() => setSidebarOpen(false)}
          >
            <Avatar
              name={meQuery.data.username}
              src={meQuery.data.profile_photo_link}
              size="sm"
            />
            <span>
              <strong>{meQuery.data.username}</strong>
              <small>{meQuery.data.email}</small>
            </span>
          </NavLink>
        ) : null}

        <div className="sidebar-section">
          <div className="sidebar-section-heading">
            <span>Study spaces</span>
            <button
              type="button"
              className="icon-button"
              aria-label="Create workspace"
              title="Create workspace"
              onClick={() => setIsCreating(true)}
            >
              <Plus size={16} />
            </button>
          </div>

          <div className="workspace-nav">
            {workspacesQuery.isLoading ? (
              <span className="sidebar-muted">Loading spaces...</span>
            ) : null}
            {workspaces.map((workspace) => (
              <NavLink
                key={workspace.workspace_id}
                to={`/app/workspaces/${workspace.workspace_id}`}
                onClick={() => setSidebarOpen(false)}
                className={({ isActive }) =>
                  clsx(
                    'workspace-nav-item',
                    isActive || activeWorkspaceId === workspace.workspace_id
                      ? 'active'
                      : undefined,
                  )
                }
              >
                <span className="workspace-marker" aria-hidden="true">
                  <AppIcon name="study-space" size={20} />
                </span>
                <span className="workspace-nav-copy">
                  <strong>{workspace.title}</strong>
                  <small>
                    <CalendarDays size={12} />
                    {compactDate(workspace.deadline)}
                  </small>
                </span>
              </NavLink>
            ))}
            {!workspacesQuery.isLoading && workspaces.length === 0 ? (
              <button
                type="button"
                className="workspace-nav-empty"
                onClick={() => setIsCreating(true)}
              >
                <Plus size={14} />
                Create your first space
              </button>
            ) : null}
          </div>
        </div>

        <div className="sidebar-meta">
          <span>
            <Sparkles size={13} />
            {workspaces.length} spaces
          </span>
          <span>
            <ChevronsLeft size={13} />
            {sharedCount} shared
          </span>
        </div>

        <div className="sidebar-actions">
          <button type="button" className="sidebar-action" onClick={toggleTheme}>
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
            {theme === 'dark' ? 'Light theme' : 'Dark theme'}
          </button>
          <NavLink
            className="sidebar-action"
            to="/settings"
            onClick={() => setSidebarOpen(false)}
          >
            <Settings size={16} />
            Settings
          </NavLink>
          <button type="button" className="sidebar-action" onClick={handleLogout}>
            <LogOut size={16} />
            Log out
          </button>
        </div>
      </aside>

      {sidebarOpen ? (
        <button
          type="button"
          className="sidebar-backdrop"
          aria-label="Close sidebar"
          onClick={() => setSidebarOpen(false)}
        />
      ) : null}

      <main className="app-main" data-route={location.pathname}>
        <Outlet context={{ openCreateWorkspace: () => setIsCreating(true) }} />
      </main>

      <CreateWorkspaceDialog
        open={isCreating}
        onClose={() => setIsCreating(false)}
        onCreated={(workspaceId) => {
          queryClient.invalidateQueries({ queryKey: ['workspaces'] })
          navigate(`/app/workspaces/${workspaceId}`)
        }}
      />
    </div>
  )
}

function CreateWorkspaceDialog({
  open,
  onClose,
  onCreated,
}: {
  open: boolean
  onClose: () => void
  onCreated: (workspaceId: number) => void
}) {
  const queryClient = useQueryClient()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [deadline, setDeadline] = useState('')

  const createMutation = useMutation({
    mutationFn: () =>
      api.createWorkspace({
        title: title.trim(),
        description: normalizeOptional(description),
        deadline: dateInputToIso(deadline),
      }),
    onSuccess: (workspace) => {
      toast.success('Study space created')
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
      setTitle('')
      setDescription('')
      setDeadline('')
      onClose()
      onCreated(workspace.workspace_id)
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  if (!open) return null

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!title.trim()) return
    createMutation.mutate()
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <form className="modal-panel" onSubmit={submit}>
        <div className="modal-heading">
          <div>
            <h2>New study space</h2>
            <p>Give this project a clear place to grow.</p>
          </div>
          <button
            type="button"
            className="icon-button"
            aria-label="Close dialog"
            title="Close dialog"
            onClick={onClose}
          >
            <X size={16} />
          </button>
        </div>

        <label className="field-label">
          Title
          <input
            className="text-input"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="Algorithms sprint"
            autoFocus
          />
        </label>
        <label className="field-label">
          Description
          <textarea
            className="text-input text-area"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="What are you studying, and what needs to happen?"
          />
        </label>
        <label className="field-label">
          Deadline
          <input
            className="text-input"
            type="date"
            value={deadline}
            onChange={(event) => setDeadline(event.target.value)}
          />
        </label>

        <div className="modal-actions">
          <button type="button" className="button button-ghost" onClick={onClose}>
            Cancel
          </button>
          <button
            type="submit"
            className="button button-primary"
            disabled={!title.trim() || createMutation.isPending}
          >
            Create space
          </button>
        </div>
      </form>
    </div>
  )
}
