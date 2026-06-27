import { lazy, Suspense } from 'react'
import type { ReactNode } from 'react'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom'

import { useAuth } from './auth/useAuth'
import { AppShell } from './components/AppShell'
import { LoadingView } from './components/StatusView'

const AuthPage = lazy(() =>
  import('./pages/AuthPage').then((module) => ({ default: module.AuthPage })),
)
const InvitePage = lazy(() =>
  import('./pages/InvitePage').then((module) => ({ default: module.InvitePage })),
)
const NotFoundPage = lazy(() =>
  import('./pages/NotFoundPage').then((module) => ({
    default: module.NotFoundPage,
  })),
)
const OAuthCallbackPage = lazy(() =>
  import('./pages/OAuthCallbackPage').then((module) => ({
    default: module.OAuthCallbackPage,
  })),
)
const SettingsPage = lazy(() =>
  import('./pages/SettingsPage').then((module) => ({
    default: module.SettingsPage,
  })),
)
const TaskPage = lazy(() =>
  import('./pages/TaskPage').then((module) => ({ default: module.TaskPage })),
)
const WorkspaceHomePage = lazy(() =>
  import('./pages/WorkspaceHomePage').then((module) => ({
    default: module.WorkspaceHomePage,
  })),
)
const WorkspacePage = lazy(() =>
  import('./pages/WorkspacePage').then((module) => ({
    default: module.WorkspacePage,
  })),
)

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
    <Suspense fallback={<LoadingView label="Opening StudySync" />}>
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
    </Suspense>
  )
}
