import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { AlertCircle, Loader2 } from 'lucide-react'
import { toast } from 'sonner'

import { useAuth } from '../auth/useAuth'
import {
  clearPendingInvite,
  getPendingInvite,
  storePendingInvite,
} from '../auth/token'
import { BrandLogo } from '../components/BrandLogo'
import { api, apiErrorToMessage, getApiBaseUrl } from '../lib/api'

type AuthPageProps = {
  mode: 'login' | 'register'
}

type LocationState = {
  from?: {
    pathname?: string
  }
  pendingInvite?: string
}

export function AuthPage({ mode }: AuthPageProps) {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const state = location.state as LocationState | null
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const isRegister = mode === 'register'
  const passwordIsStrong =
    password.length >= 8 && /[A-Za-z]/.test(password) && /\d/.test(password)
  const canSubmit = isRegister
    ? username.trim() &&
      email.trim() &&
      passwordIsStrong &&
      password === confirmPassword
    : identifier.trim() && password

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    if (!canSubmit) return

    setIsSubmitting(true)
    try {
      const response = isRegister
        ? await api.register({
            username: username.trim(),
            email: email.trim(),
            password,
          })
        : await api.login(identifier.trim(), password)

      login(response.access_token)

      const inviteToken = state?.pendingInvite ?? getPendingInvite()
      if (inviteToken) {
        storePendingInvite(inviteToken)
        try {
          await api.acceptInvite(inviteToken)
          clearPendingInvite()
          toast.success('Workspace invite accepted')
        } catch (inviteError) {
          toast.error(apiErrorToMessage(inviteError))
        }
      }

      navigate(state?.from?.pathname ?? '/app', { replace: true })
    } catch (authError) {
      setError(apiErrorToMessage(authError))
    } finally {
      setIsSubmitting(false)
    }
  }

  function startOAuth(provider: 'google' | 'github') {
    const inviteToken = state?.pendingInvite ?? getPendingInvite()
    if (inviteToken) {
      storePendingInvite(inviteToken)
    }

    window.location.href = `${getApiBaseUrl()}/login/${provider}`
  }

  return (
    <main className="auth-page">
      <section className="auth-panel">
        <Link className="auth-brand" to="/">
          <BrandLogo />
          <span>StudySync</span>
        </Link>

        <div className="auth-copy">
          <h1>{isRegister ? 'Create your study workspace' : 'Welcome back'}</h1>
          <p>
            {isRegister
              ? 'Organize spaces, goals, and notes for the way you learn.'
              : 'Pick up your study spaces right where you left them.'}
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {isRegister ? (
            <>
              <label className="field-label">
                Username
                <input
                  className="text-input"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  autoComplete="username"
                  placeholder="lusparkl"
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
                  placeholder="you@example.com"
                />
              </label>
            </>
          ) : (
            <label className="field-label">
              Email or username
              <input
                className="text-input"
                value={identifier}
                onChange={(event) => setIdentifier(event.target.value)}
                autoComplete="username"
                placeholder="you@example.com"
                autoFocus
              />
            </label>
          )}

          <label className="field-label">
            Password
            <input
              className="text-input"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete={isRegister ? 'new-password' : 'current-password'}
              placeholder="At least 8 characters"
            />
          </label>

          {isRegister ? (
            <>
              <label className="field-label">
                Confirm password
                <input
                  className="text-input"
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  autoComplete="new-password"
                  placeholder="Repeat password"
                />
              </label>
              <p className="field-hint">
                Use at least 8 characters with a letter and a number.
              </p>
            </>
          ) : null}

          {error ? (
            <div className="form-error">
              <AlertCircle size={16} />
              {error}
            </div>
          ) : null}

          <button
            type="submit"
            className="button button-primary auth-submit"
            disabled={!canSubmit || isSubmitting}
          >
            {isSubmitting ? <Loader2 className="spin" size={16} /> : null}
            {isRegister ? 'Create account' : 'Log in'}
          </button>
        </form>

        <div className="oauth-divider">
          <span>or continue with</span>
        </div>

        <div className="oauth-actions">
          <button
            type="button"
            className="button button-secondary oauth-button"
            onClick={() => startOAuth('google')}
          >
            <span className="oauth-mark google-mark" aria-hidden="true">
              G
            </span>
            Google
          </button>
          <button
            type="button"
            className="button button-secondary oauth-button"
            onClick={() => startOAuth('github')}
          >
            <span className="oauth-mark github-mark" aria-hidden="true">
              GH
            </span>
            GitHub
          </button>
        </div>

        <p className="auth-switch">
          {isRegister ? 'Already have an account?' : 'New to StudySync?'}{' '}
          <Link to={isRegister ? '/login' : '/register'}>
            {isRegister ? 'Log in' : 'Create account'}
          </Link>
        </p>
      </section>
    </main>
  )
}
