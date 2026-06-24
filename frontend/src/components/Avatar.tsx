import { useState } from 'react'

import { initials } from '../lib/format'

type AvatarProps = {
  name: string
  src?: string | null
  size?: 'sm' | 'md'
}

export function Avatar({ name, src, size = 'md' }: AvatarProps) {
  const [failedSrc, setFailedSrc] = useState<string | null>(null)
  const imageSrc = normalizeAvatarSrc(src)
  const canShowImage = imageSrc && imageSrc !== failedSrc

  return canShowImage ? (
    <img
      className={`avatar avatar-${size}`}
      src={imageSrc}
      alt=""
      referrerPolicy="no-referrer"
      onError={() => setFailedSrc(imageSrc)}
    />
  ) : (
    <span className={`avatar avatar-${size}`} aria-hidden="true">
      {initials(name)}
    </span>
  )
}

function normalizeAvatarSrc(src?: string | null) {
  if (!src) return null

  try {
    const url = new URL(src)
    url.pathname = url.pathname.replace(/\/{2,}/g, '/')
    return url.toString()
  } catch {
    return src
  }
}
