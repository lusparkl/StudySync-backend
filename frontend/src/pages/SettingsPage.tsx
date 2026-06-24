import { useState } from 'react'
import type { FormEvent } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { LogOut, Save, UserRound } from 'lucide-react'
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

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!username.trim() || !email.trim()) return
    updateMutation.mutate()
  }

  return (
    <>
      <div className="profile-preview">
        <Avatar name={user.username} src={user.profile_photo_link} size="md" />
        <div>
          <h2>{user.username}</h2>
          <p>{user.email}</p>
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
