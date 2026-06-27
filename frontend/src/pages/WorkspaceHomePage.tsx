import { Navigate, useOutletContext } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Plus } from 'lucide-react'

import type { ShellContext } from '../components/AppShell'
import { AppIcon } from '../components/AppIcon'
import { EmptyState } from '../components/EmptyState'
import { LoadingView } from '../components/StatusView'
import { api } from '../lib/api'

export function WorkspaceHomePage() {
  const { openCreateWorkspace } = useOutletContext<ShellContext>()
  const workspacesQuery = useQuery({
    queryKey: ['workspaces'],
    queryFn: api.getWorkspaces,
  })

  if (workspacesQuery.isLoading || workspacesQuery.isFetching) {
    return <LoadingView label="Loading study spaces" />
  }

  const firstWorkspace = workspacesQuery.data?.[0]
  if (firstWorkspace) {
    return (
      <Navigate to={`/app/workspaces/${firstWorkspace.workspace_id}`} replace />
    )
  }

  return (
    <EmptyState
      icon={<AppIcon name="study-space" size={44} />}
      title="Create your first study space"
      description="StudySync starts with a shared space for one topic, course, exam, or project."
      action={
        <button
          type="button"
          className="button button-primary"
          onClick={openCreateWorkspace}
        >
          <Plus size={16} />
          New study space
        </button>
      }
    />
  )
}
