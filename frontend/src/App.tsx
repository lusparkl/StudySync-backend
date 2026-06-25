import type { ReactNode } from 'react'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom'

import { useAuth } from './auth/useAuth'
import { AppShell } from './components/AppShell'
import { AuthPage } from './pages/AuthPage'
import { InvitePage } from './pages/InvitePage'
import { NotFoundPage } from './pages/NotFoundPage'
import { OAuthCallbackPage } from './pages/OAuthCallbackPage'
import { SettingsPage } from './pages/SettingsPage'
import { TaskPage } from './pages/TaskPage'
import { WorkspaceHomePage } from './pages/WorkspaceHomePage'
import { WorkspacePage } from './pages/WorkspacePage'

function RequireAuth() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  return <AppShell />
}

function PublicOnly({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth()

  if (isAuthenticated) {
    return <Navigate to="/app" replace />
  }

  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/app" replace />} />
      <Route
        path="/login"
        element={
          <PublicOnly>
            <AuthPage mode="login" />
          </PublicOnly>
        }
      />
      <Route
        path="/register"
        element={
          <PublicOnly>
            <AuthPage mode="register" />
          </PublicOnly>
        }
      />
      <Route path="/invite/:inviteToken" element={<InvitePage />} />
      <Route path="/oauth/callback" element={<OAuthCallbackPage />} />
      <Route element={<RequireAuth />}>
        <Route path="/app" element={<WorkspaceHomePage />} />
        <Route path="/app/workspaces/:workspaceId" element={<WorkspacePage />} />
        <Route
          path="/app/workspaces/:workspaceId/tasks/:taskId"
          element={<TaskPage />}
        />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
