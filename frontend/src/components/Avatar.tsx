import { initials } from '../lib/format'

type AvatarProps = {
  name: string
  src?: string | null
  size?: 'sm' | 'md'
}

export function Avatar({ name, src, size = 'md' }: AvatarProps) {
  return src ? (
    <img className={`avatar avatar-${size}`} src={src} alt="" />
  ) : (
    <span className={`avatar avatar-${size}`} aria-hidden="true">
      {initials(name)}
    </span>
  )
}

