import { Toaster } from 'sonner'

import { useTheme } from '../theme/useTheme'

export function ThemedToaster() {
  const { theme } = useTheme()

  return <Toaster richColors theme={theme} position="top-right" closeButton />
}

