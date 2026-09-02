import { useMDXComponents as getThemeComponents } from 'nextra-theme-docs'
import { PasswordGate } from './components/PasswordGate'
import { HeroSection } from './components/HeroSection'
import { PrepCard } from './components/PrepCard'

const themeComponents = getThemeComponents()

export function useMDXComponents(components) {
  return {
    ...themeComponents,
    PasswordGate,
    HeroSection,
    PrepCard,
    ...components
  }
}
