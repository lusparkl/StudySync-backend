import { useEffect, useRef } from 'react'
import { AlertTriangle, Loader2, X } from 'lucide-react'
import clsx from 'clsx'

type ConfirmDialogProps = {
  open: boolean
  title: string
  description: string
  confirmLabel?: string
  cancelLabel?: string
  tone?: 'default' | 'danger'
  busy?: boolean
  onCancel: () => void
  onConfirm: () => void
}

export function ConfirmDialog({
  open,
  title,
  description,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  tone = 'default',
  busy = false,
  onCancel,
  onConfirm,
}: ConfirmDialogProps) {
  const confirmButtonRef = useRef<HTMLButtonElement | null>(null)

  useEffect(() => {
    if (!open) return undefined

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape' && !busy) {
        onCancel()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [busy, onCancel, open])

  useEffect(() => {
    if (!open) return undefined

    const frameId = window.requestAnimationFrame(() => {
      confirmButtonRef.current?.focus()
    })

    return () => window.cancelAnimationFrame(frameId)
  }, [open])

  if (!open) return null

  return (
    <div
      className="modal-backdrop confirm-backdrop"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !busy) {
          onCancel()
        }
      }}
    >
      <section
        className={clsx('modal-panel confirm-panel', `confirm-panel-${tone}`)}
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-dialog-title"
        aria-describedby="confirm-dialog-description"
      >
        <div className="confirm-icon" aria-hidden="true">
          <AlertTriangle size={20} />
        </div>

        <div className="modal-heading confirm-heading">
          <div>
            <h2 id="confirm-dialog-title">{title}</h2>
            <p id="confirm-dialog-description">{description}</p>
          </div>
          <button
            type="button"
            className="icon-button"
            aria-label="Close dialog"
            title="Close dialog"
            onClick={onCancel}
            disabled={busy}
          >
            <X size={16} />
          </button>
        </div>

        <div className="modal-actions confirm-actions">
          <button
            type="button"
            className="button button-ghost"
            onClick={onCancel}
            disabled={busy}
          >
            {cancelLabel}
          </button>
          <button
            ref={confirmButtonRef}
            type="button"
            className={clsx('button', tone === 'danger' ? 'button-danger' : 'button-primary')}
            onClick={onConfirm}
            disabled={busy}
          >
            {busy ? <Loader2 className="spin" size={16} /> : null}
            {confirmLabel}
          </button>
        </div>
      </section>
    </div>
  )
}
