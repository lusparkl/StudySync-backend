import { AlertTriangle, Loader2 } from 'lucide-react'

export function LoadingView({ label = 'Loading StudySync' }: { label?: string }) {
  return (
    <div className="status-view">
      <Loader2 className="spin" size={22} aria-hidden="true" />
      <span>{label}</span>
    </div>
  )
}

export function ErrorView({
  title = 'Something went wrong',
  message,
}: {
  title?: string
  message: string
}) {
  return (
    <section className="status-view status-view-error">
      <AlertTriangle size={22} aria-hidden="true" />
      <div>
        <h2>{title}</h2>
        <p>{message}</p>
      </div>
    </section>
  )
}

