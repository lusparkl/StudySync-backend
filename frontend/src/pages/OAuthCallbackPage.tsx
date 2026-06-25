import { useEffect, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Loader2 } from 'lucide-react'
import { toast } from 'sonner'

import { useAuth } from '../auth/useAuth'
import {
  clearPendingInvite,
  getPendingInvite,
  storePendingInvite,
} from '../auth/token'
import { BrandLogo } from '../components/BrandLogo'
import { api, apiErrorToMessage } from '../lib/api'

export function OAuthCallbackPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const handledRef = useRef(false)

  useEffect(() => {
    if (handledRef.current) return
    handledRef.current = true

    async function finishOauth() {
      const token = searchParams.get('access_token')
      const error = searchParams.get('error')

      if (error) {
        toast.error(error)
        navigate('/login', { replace: true })
        return
      }

      if (!token) {
        toast.error('OAuth login did not return a session token.')
        navigate('/login', { replace: true })
        return
      }

      login(token)

      const inviteToken = getPendingInvite()
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

      navigate('/app', { replace: true })
    }

    void finishOauth()
  }, [login, navigate, searchParams])

  return (
    <main className="auth-page">
      <section className="auth-panel oauth-callback-panel">
        <BrandLogo />
        <Loader2 className="spin" size={22} />
        <h1>Signing you in</h1>
        <p>Finishing your OAuth session and opening StudySync.</p>
      </section>
    </main>
  )
}
