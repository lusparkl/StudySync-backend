import logo from '../assets/logo.svg'
import logoWhite from '../assets/logo_white.svg'
import { useTheme } from '../theme/useTheme'

export function BrandLogo() {
  const { theme } = useTheme()
  const logoSrc = theme === 'dark' ? logoWhite : logo

  return (
    <span className="brand-mark" aria-hidden="true">
      <img className="brand-logo" src={logoSrc} alt="" />
    </span>
  )
}
