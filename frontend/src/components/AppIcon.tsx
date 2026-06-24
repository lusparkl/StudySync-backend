import clsx from 'clsx'

type AppIconName = 'note' | 'study-space' | 'task'

type AppIconProps = {
  name: AppIconName
  size?: number
  className?: string
}

export function AppIcon({ name, size = 16, className }: AppIconProps) {
  return (
    <svg
      className={clsx('asset-icon', className)}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden="true"
      focusable="false"
    >
      {name === 'study-space' ? <StudySpaceIcon /> : null}
      {name === 'task' ? <TaskIcon /> : null}
      {name === 'note' ? <NoteIcon /> : null}
    </svg>
  )
}

function StudySpaceIcon() {
  return (
    <>
      <path
        d="M4.25 6.9c0-1.63 1.32-2.95 2.95-2.95h9.1c1.63 0 2.95 1.32 2.95 2.95v10.2c0 1.63-1.32 2.95-2.95 2.95H7.2a2.95 2.95 0 0 1-2.95-2.95V6.9Z"
        fill="currentColor"
        opacity="0.13"
      />
      <path
        d="M7.15 4.05h9.25c1.57 0 2.85 1.28 2.85 2.85v10.2c0 1.57-1.28 2.85-2.85 2.85H7.15a2.85 2.85 0 0 1-2.85-2.85V6.9c0-1.57 1.28-2.85 2.85-2.85Z"
        stroke="currentColor"
        strokeWidth="1.65"
      />
      <path
        d="M7.65 8.15h8.7M7.65 11.35h8.7M7.65 14.55h5.15"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.65"
      />
      <path
        d="M6.65 19.55c.62-1.15 1.67-1.72 3.15-1.72h5.35"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.65"
      />
    </>
  )
}

function TaskIcon() {
  return (
    <>
      <path
        d="M5 5.6c0-1.22.98-2.2 2.2-2.2h9.6c1.22 0 2.2.98 2.2 2.2v12.8c0 1.22-.98 2.2-2.2 2.2H7.2A2.2 2.2 0 0 1 5 18.4V5.6Z"
        fill="currentColor"
        opacity="0.13"
      />
      <path
        d="M7.2 3.4h9.6c1.22 0 2.2.98 2.2 2.2v12.8c0 1.22-.98 2.2-2.2 2.2H7.2A2.2 2.2 0 0 1 5 18.4V5.6c0-1.22.98-2.2 2.2-2.2Z"
        stroke="currentColor"
        strokeWidth="1.65"
      />
      <path
        d="m8.1 8.1 1.05 1.05 2.1-2.25M13.25 8.25h2.9M8.1 13.05l1.05 1.05 2.1-2.25M13.25 13.2h2.9M8.2 17.25h7.95"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.65"
      />
    </>
  )
}

function NoteIcon() {
  return (
    <>
      <path
        d="M6.05 4.95c0-1.1.9-2 2-2h5.9l4 4v12.1c0 1.1-.9 2-2 2h-7.9c-1.1 0-2-.9-2-2V4.95Z"
        fill="currentColor"
        opacity="0.13"
      />
      <path
        d="M8.05 2.95h5.9l4 4v12.1c0 1.1-.9 2-2 2h-7.9c-1.1 0-2-.9-2-2V4.95c0-1.1.9-2 2-2Z"
        stroke="currentColor"
        strokeLinejoin="round"
        strokeWidth="1.65"
      />
      <path
        d="M13.95 3.1v3.25c0 .55.45 1 1 1h2.85"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.65"
      />
      <path
        d="M8.8 11.05h6.45M8.8 14.25h5.3M8.8 17.45h3.45"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.65"
      />
    </>
  )
}
