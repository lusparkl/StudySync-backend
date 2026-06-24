import type { CSSProperties } from 'react'
import clsx from 'clsx'

import notesIcon from '../assets/notes.svg'
import studySpacesIcon from '../assets/study_spaces.svg'
import tasksIcon from '../assets/tasks.svg'

type AppIconName = 'note' | 'study-space' | 'task'

type AppIconProps = {
  name: AppIconName
  size?: number
  className?: string
}

const icons: Record<AppIconName, string> = {
  note: notesIcon,
  'study-space': studySpacesIcon,
  task: tasksIcon,
}

export function AppIcon({ name, size = 16, className }: AppIconProps) {
  const src = icons[name]
  const style = {
    width: size,
    height: size,
    WebkitMaskImage: `url(${src})`,
    maskImage: `url(${src})`,
  } satisfies CSSProperties

  return (
    <span
      className={clsx('asset-icon', className)}
      style={style}
      aria-hidden="true"
    />
  )
}
