import { Link } from 'react-router-dom'
import { FileQuestion } from 'lucide-react'

import { EmptyState } from '../components/EmptyState'

export function NotFoundPage() {
  return (
    <main className="standalone-page">
      <EmptyState
        icon={<FileQuestion size={26} />}
        title="Page not found"
        description="This route does not exist, or the study space moved."
        action={
          <Link className="button button-primary" to="/app">
            Back to StudySync
          </Link>
        }
      />
    </main>
  )
}

