import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react'
import type { ReactNode } from 'react'
import { useQueryClient } from '@tanstack/react-query'

import { AuthContext } from './auth-context'
import { clearStoredToken, getStoredToken, storeToken } from './token'

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient()
  const [token, setToken] = useState(() => getStoredToken())

  const logout = useCallback(() => {
    clearStoredToken()
    setToken(null)
    queryClient.clear()
  }, [queryClient])

  const login = useCallback(
    (nextToken: string) => {
      storeToken(nextToken)
      setToken(nextToken)
      queryClient.invalidateQueries()
    },
    [queryClient],
  )

  useEffect(() => {
    window.addEventListener('studysync:unauthorized', logout)
    return () => window.removeEventListener('studysync:unauthorized', logout)
  }, [logout])

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      login,
      logout,
    }),
    [login, logout, token],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
