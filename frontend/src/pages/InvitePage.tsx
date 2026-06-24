import { useEffect } from 'react'
import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { UserPlus } from 'lucide-react'
import { toast } from 'sonner'

import { useAuth } from '../auth/useAuth'
import { clearPendingInvite, storePendingInvite } from '../auth/token'
import { EmptyState } from '../components/EmptyState'
import { ErrorView, LoadingView } from '../components/StatusView'
import { api, apiErrorToMessage } from '../lib/api'

export function InvitePage() {
  const { inviteToken } = useParams()
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const acceptMutation = useMutation({
    mutationFn: (token: string) => api.acceptInvite(token),
    onSuccess: () => {
      clearPendingInvite()
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
      queryClient.invalidateQueries({ queryKey: ['me'] })
      toast.success('Workspace invite accepted')
      navigate('/app', { replace: true })
    },
  })
  const {
    mutate: acceptInvite,
    isPending: isAccepting,
    isError,
    error,
  } = acceptMutation

  useEffect(() => {
    if (!inviteToken || !isAuthenticated || isAccepting) return
    acceptInvite(inviteToken)
  }, [acceptInvite, inviteToken, isAccepting, isAuthenticated])

  if (!inviteToken) {
    return (
      <main className="standalone-page">
        <ErrorView
          title="Invite not found"
          message="This invite link does not include a token."
        />
      </main>
    )
  }

  if (!isAuthenticated) {
    storePendingInvite(inviteToken)
    return (
      <Navigate
        to="/login"
        replace
        state={{ pendingInvite: inviteToken, from: { pathname: '/app' } }}
      />
    )
  }

  if (isError) {
    return (
      <main className="standalone-page">
        <ErrorView
          title="Invite could not be accepted"
          message={apiErrorToMessage(error)}
        />
      </main>
    )
  }

  return (
    <main className="standalone-page">
      {isAccepting ? (
        <LoadingView label="Joining workspace" />
      ) : (
        <EmptyState
          icon={<UserPlus size={26} />}
          title="Joining workspace"
          description="StudySync is adding this shared space to your sidebar."
        />
      )}
    </main>
  )
}
