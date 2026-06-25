import { format, isValid, parseISO } from 'date-fns'

export function compactDate(value: string | null | undefined) {
  if (!value) return 'No deadline'

  const date = parseISO(value)
  if (!isValid(date)) return 'No deadline'

  return format(date, 'MMM d, yyyy')
}

export function dateInputValue(value: string | null | undefined) {
  if (!value) return ''

  const date = parseISO(value)
  if (!isValid(date)) return ''

  return format(date, 'yyyy-MM-dd')
}

export function dateInputToIso(value: string) {
  if (!value) return null

  return new Date(`${value}T09:00:00`).toISOString()
}

export function initials(name: string) {
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('')
}

export function normalizeOptional(value: string) {
  const trimmed = value.trim()
  return trimmed.length ? trimmed : null
}

