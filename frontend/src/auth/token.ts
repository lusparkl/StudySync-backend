export const TOKEN_STORAGE_KEY = 'studysync.access_token'
export const PENDING_INVITE_KEY = 'studysync.pending_invite'

export function getStoredToken() {
  return window.localStorage.getItem(TOKEN_STORAGE_KEY)
}

export function storeToken(token: string) {
  window.localStorage.setItem(TOKEN_STORAGE_KEY, token)
}

export function clearStoredToken() {
  window.localStorage.removeItem(TOKEN_STORAGE_KEY)
}

export function storePendingInvite(token: string) {
  window.localStorage.setItem(PENDING_INVITE_KEY, token)
}

export function getPendingInvite() {
  return window.localStorage.getItem(PENDING_INVITE_KEY)
}

export function clearPendingInvite() {
  window.localStorage.removeItem(PENDING_INVITE_KEY)
}

