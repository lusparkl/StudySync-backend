import { useState } from 'react'
import type { FormEvent } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ImageUp, LogOut, Save, Trash2, UserRound } from 'lucide-react'
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
      <header className="page-header">
        <div className="page-kicker">
          <UserRound size={16} />
          Settings
        </div>
        <h1>Profile</h1>
        <p>Keep the identity attached to your study spaces current.</p>
      </header>

      <section className="settings-layout">
        <SettingsForm user={meQuery.data} onLogout={logout} />
      </section>
    </article>
  )
}

function SettingsForm({
  user,
  onLogout,
}: {
  user: UserPrivate
  onLogout: () => void
}) {
  const queryClient = useQueryClient()
  const [username, setUsername] = useState(user.username)
  const [email, setEmail] = useState(user.email)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  const avatarSrc = previewUrl ?? user.profile_photo_link

  const updateMutation = useMutation({
    mutationFn: () =>
      api.updateMe({
        username: username.trim(),
        email: email.trim(),
      }),
    onSuccess: () => {
      toast.success('Profile updated')
      queryClient.invalidateQueries({ queryKey: ['me'] })
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
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

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!username.trim() || !email.trim()) return
    updateMutation.mutate()
  }

  return (
    <>
      <div className="profile-preview">
        <div className="avatar-editor">
          <Avatar name={user.username} src={avatarSrc} size="md" />
          <label className="avatar-upload-button" title="Upload profile photo">
            <ImageUp size={16} />
            <input
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(event) => uploadPhoto(event.target.files?.[0])}
              disabled={uploadPhotoMutation.isPending}
            />
          </label>
        </div>
        <div>
          <h2>{user.username}</h2>
          <p>{user.email}</p>
          <div className="profile-photo-actions">
            <label className="button button-secondary">
              <ImageUp size={16} />
              Upload photo
              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={(event) => uploadPhoto(event.target.files?.[0])}
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

      <form className="settings-form" onSubmit={submit}>
        <label className="field-label">
          Username
          <input
            className="text-input"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </label>
        <label className="field-label">
          Email
          <input
            className="text-input"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>
        <label className="field-label">
          Backend URL
          <input className="text-input" value={getApiBaseUrl()} readOnly />
        </label>

        <div className="settings-actions">
          <button
            type="submit"
            className="button button-primary"
            disabled={!username.trim() || !email.trim() || updateMutation.isPending}
          >
            <Save size={16} />
            Save changes
          </button>
          <button
            type="button"
            className="button button-secondary"
            onClick={onLogout}
          >
            <LogOut size={16} />
            Log out
          </button>
        </div>
      </form>
    </>
  )
}
