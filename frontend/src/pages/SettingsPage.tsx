import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  BadgeCheck,
  Camera,
  Check,
  Clipboard,
  GitBranch,
  Globe2,
  ImageUp,
  KeyRound,
  Loader2,
  LogOut,
  Mail,
  Moon,
  Palette,
  Save,
  ShieldCheck,
  Sun,
  Trash2,
  UserRound,
} from 'lucide-react'
import clsx from 'clsx'
import { toast } from 'sonner'

import { useAuth } from '../auth/useAuth'
import { Avatar } from '../components/Avatar'
import { ErrorView, LoadingView } from '../components/StatusView'
import {
  api,
  apiErrorToMessage,
  getApiBaseUrl,
  type UserPrivate,
} from '../lib/api'
import { useTheme } from '../theme/useTheme'

export function SettingsPage() {
  const { logout } = useAuth()
  const meQuery = useQuery({
    queryKey: ['me'],
    queryFn: api.getMe,
  })

  if (meQuery.isLoading) {
    return <LoadingView label="Loading profile" />
  }

  if (meQuery.isError || !meQuery.data) {
    return (
      <ErrorView
        title="Profile not available"
        message={apiErrorToMessage(meQuery.error)}
      />
    )
  }

  return (
    <article className="page settings-page">
      <header className="page-header settings-header">
        <div className="page-kicker">
          <UserRound size={16} />
          Settings
        </div>
        <h1>Account settings</h1>
        <p>Manage the profile and preferences attached to your study spaces.</p>
      </header>

      <section className="settings-layout">
        <nav className="settings-nav" aria-label="Settings sections">
          <a href="#profile">
            <UserRound size={15} />
            Profile
          </a>
          <a href="#appearance">
            <Palette size={15} />
            Appearance
          </a>
          <a href="#security">
            <ShieldCheck size={15} />
            Security
          </a>
          <a href="#system">
            <Globe2 size={15} />
            System
          </a>
        </nav>

        <SettingsConsole user={meQuery.data} onLogout={logout} />
      </section>
    </article>
  )
}

function SettingsConsole({
  user,
  onLogout,
}: {
  user: UserPrivate
  onLogout: () => void
}) {
  const queryClient = useQueryClient()
  const { theme, setTheme } = useTheme()
  const [username, setUsername] = useState(user.username)
  const [email, setEmail] = useState(user.email)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [apiCopied, setApiCopied] = useState(false)
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const avatarSrc = previewUrl ?? user.profile_photo_link
  const hasProfileChanges =
    username.trim() !== user.username || email.trim() !== user.email
  const passwordIsStrong =
    newPassword.length >= 8 && /[A-Za-z]/.test(newPassword) && /\d/.test(newPassword)
  const passwordReady =
    Boolean(oldPassword) && passwordIsStrong && newPassword === confirmPassword

  useEffect(
    () => () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl)
    },
    [previewUrl],
  )

  const updateMutation = useMutation({
    mutationFn: () =>
      api.updateMe({
        username: username.trim(),
        email: email.trim(),
      }),
    onSuccess: (updatedUser) => {
      toast.success('Profile updated')
      setUsername(updatedUser.username)
      setEmail(updatedUser.email)
      queryClient.invalidateQueries({ queryKey: ['me'] })
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const changePasswordMutation = useMutation({
    mutationFn: () =>
      api.changePassword({
        old_password: oldPassword,
        new_password: newPassword,
      }),
    onSuccess: () => {
      toast.success('Password updated')
      setOldPassword('')
      setNewPassword('')
      setConfirmPassword('')
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  const uploadPhotoMutation = useMutation({
    mutationFn: (file: File) => api.updateProfilePicture(file),
    onSuccess: () => {
      toast.success('Profile photo updated')
      setPreviewUrl((current) => {
        if (current) URL.revokeObjectURL(current)
        return null
      })
      queryClient.invalidateQueries({ queryKey: ['me'] })
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
    },
    onError: (error) => {
      setPreviewUrl((current) => {
        if (current) URL.revokeObjectURL(current)
        return null
      })
      toast.error(apiErrorToMessage(error))
    },
  })

  const deletePhotoMutation = useMutation({
    mutationFn: api.deleteProfilePicture,
    onSuccess: () => {
      toast.success('Profile photo removed')
      setPreviewUrl((current) => {
        if (current) URL.revokeObjectURL(current)
        return null
      })
      queryClient.invalidateQueries({ queryKey: ['me'] })
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
    },
    onError: (error) => toast.error(apiErrorToMessage(error)),
  })

  function uploadPhoto(file: File | undefined) {
    if (!file) return

    setPreviewUrl((current) => {
      if (current) URL.revokeObjectURL(current)
      return URL.createObjectURL(file)
    })
    uploadPhotoMutation.mutate(file)
  }

  function submitProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!username.trim() || !email.trim() || !hasProfileChanges) return
    updateMutation.mutate()
  }

  function submitPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!passwordReady) return
    changePasswordMutation.mutate()
  }

  async function copyApiUrl() {
    try {
      await navigator.clipboard.writeText(getApiBaseUrl())
      setApiCopied(true)
      toast.success('API URL copied')
      window.setTimeout(() => setApiCopied(false), 1600)
    } catch {
      toast.message('API URL', { description: getApiBaseUrl() })
    }
  }

  return (
    <div className="settings-stack">
      <section className="settings-panel account-hero-panel" id="profile">
        <div className="profile-preview">
          <div className="avatar-editor">
            <Avatar name={user.username} src={avatarSrc} size="md" />
            <label className="avatar-upload-button" title="Upload profile photo">
              {uploadPhotoMutation.isPending ? (
                <Loader2 className="spin" size={16} />
              ) : (
                <Camera size={16} />
              )}
              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={(event) => {
                  uploadPhoto(event.target.files?.[0])
                  event.currentTarget.value = ''
                }}
                disabled={uploadPhotoMutation.isPending}
              />
            </label>
          </div>

          <div className="account-identity">
            <span className="status-pill">
              <BadgeCheck size={13} />
              Active account
            </span>
            <h2>{user.username}</h2>
            <p>{user.email}</p>
            <div className="profile-photo-actions">
              <label className="button button-secondary">
                <ImageUp size={16} />
                Upload photo
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  onChange={(event) => {
                    uploadPhoto(event.target.files?.[0])
                    event.currentTarget.value = ''
                  }}
                  disabled={uploadPhotoMutation.isPending}
                />
              </label>
              <button
                type="button"
                className="button button-ghost"
                onClick={() => deletePhotoMutation.mutate()}
                disabled={deletePhotoMutation.isPending}
              >
                <Trash2 size={16} />
                Remove
              </button>
            </div>
          </div>
        </div>

        <div className="account-meta-grid" aria-label="Account summary">
          <div>
            <span>User ID</span>
            <strong>#{user.user_id}</strong>
          </div>
          <div>
            <span>Theme</span>
            <strong>{theme === 'dark' ? 'Dark' : 'Light'}</strong>
          </div>
          <div>
            <span>Spaces</span>
            <strong>{user.workspaces.length}</strong>
          </div>
        </div>
      </section>

      <section className="settings-panel">
        <div className="settings-panel-header">
          <span className="settings-panel-icon">
            <UserRound size={18} />
          </span>
          <div>
            <h2>Profile</h2>
            <p>This is how collaborators see you in shared study spaces.</p>
          </div>
          {hasProfileChanges ? <span className="settings-state-pill">Unsaved</span> : null}
        </div>

        <form className="settings-form" onSubmit={submitProfile}>
          <div className="settings-fields-grid">
            <label className="field-label">
              Username
              <input
                className="text-input"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                autoComplete="username"
              />
            </label>
            <label className="field-label">
              Email
              <input
                className="text-input"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                autoComplete="email"
              />
            </label>
          </div>

          <div className="settings-actions">
            <button
              type="submit"
              className="button button-primary"
              disabled={
                !username.trim() ||
                !email.trim() ||
                !hasProfileChanges ||
                updateMutation.isPending
              }
            >
              {updateMutation.isPending ? (
                <Loader2 className="spin" size={16} />
              ) : (
                <Save size={16} />
              )}
              Save profile
            </button>
          </div>
        </form>
      </section>

      <section className="settings-panel" id="appearance">
        <div className="settings-panel-header">
          <span className="settings-panel-icon">
            <Palette size={18} />
          </span>
          <div>
            <h2>Appearance</h2>
            <p>Choose the workspace tone that feels best while studying.</p>
          </div>
        </div>

        <div className="theme-choice-grid" role="group" aria-label="Theme">
          <button
            type="button"
            className={clsx('theme-choice', theme === 'light' && 'active')}
            onClick={() => setTheme('light')}
          >
            <span className="theme-preview theme-preview-light" aria-hidden="true">
              <span />
              <span />
            </span>
            <span>
              <Sun size={16} />
              Light
            </span>
            {theme === 'light' ? <Check size={16} /> : null}
          </button>

          <button
            type="button"
            className={clsx('theme-choice', theme === 'dark' && 'active')}
            onClick={() => setTheme('dark')}
          >
            <span className="theme-preview theme-preview-dark" aria-hidden="true">
              <span />
              <span />
            </span>
            <span>
              <Moon size={16} />
              Dark
            </span>
            {theme === 'dark' ? <Check size={16} /> : null}
          </button>
        </div>
      </section>

      <section className="settings-panel" id="security">
        <div className="settings-panel-header">
          <span className="settings-panel-icon">
            <ShieldCheck size={18} />
          </span>
          <div>
            <h2>Security</h2>
            <p>Keep your password and sign-in methods current.</p>
          </div>
        </div>

        <form className="settings-form password-form" onSubmit={submitPassword}>
          <div className="settings-fields-grid">
            <label className="field-label">
              Current password
              <input
                className="text-input"
                type="password"
                value={oldPassword}
                onChange={(event) => setOldPassword(event.target.value)}
                autoComplete="current-password"
              />
            </label>
            <label className="field-label">
              New password
              <input
                className="text-input"
                type="password"
                value={newPassword}
                onChange={(event) => setNewPassword(event.target.value)}
                autoComplete="new-password"
              />
            </label>
            <label className="field-label">
              Confirm new password
              <input
                className="text-input"
                type="password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                autoComplete="new-password"
              />
            </label>
          </div>
          {newPassword && !passwordIsStrong ? (
            <p className="field-hint">Use at least 8 characters with letters and numbers.</p>
          ) : null}
          {confirmPassword && newPassword !== confirmPassword ? (
            <p className="field-hint warning-text">Passwords do not match.</p>
          ) : null}

          <div className="settings-actions">
            <button
              type="submit"
              className="button button-secondary"
              disabled={!passwordReady || changePasswordMutation.isPending}
            >
              {changePasswordMutation.isPending ? (
                <Loader2 className="spin" size={16} />
              ) : (
                <KeyRound size={16} />
              )}
              Change password
            </button>
          </div>
        </form>

        <div className="connection-list" aria-label="Sign-in methods">
          <div className="connection-row">
            <Mail size={17} />
            <span>
              <strong>Email and password</strong>
              <small>{user.email}</small>
            </span>
            <span className="status-pill compact">Enabled</span>
          </div>
          <div className="connection-row">
            <Globe2 size={17} />
            <span>
              <strong>Google</strong>
              <small>OAuth</small>
            </span>
            <span className="status-pill compact">Available</span>
          </div>
          <div className="connection-row">
            <GitBranch size={17} />
            <span>
              <strong>GitHub</strong>
              <small>OAuth</small>
            </span>
            <span className="status-pill compact">Available</span>
          </div>
        </div>
      </section>

      <section className="settings-panel" id="system">
        <div className="settings-panel-header">
          <span className="settings-panel-icon">
            <Globe2 size={18} />
          </span>
          <div>
            <h2>System</h2>
            <p>Local connection and session controls.</p>
          </div>
        </div>

        <label className="field-label">
          API base URL
          <div className="copy-field">
            <input className="text-input" value={getApiBaseUrl()} readOnly />
            <button
              type="button"
              className="icon-button"
              onClick={copyApiUrl}
              aria-label="Copy API URL"
              title="Copy API URL"
            >
              {apiCopied ? <Check size={16} /> : <Clipboard size={16} />}
            </button>
          </div>
        </label>

        <div className="session-row">
          <div>
            <strong>Current session</strong>
            <small>Signed in as {user.email}</small>
          </div>
          <button type="button" className="button button-secondary" onClick={onLogout}>
            <LogOut size={16} />
            Log out
          </button>
        </div>
      </section>
    </div>
  )
}
