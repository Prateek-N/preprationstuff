import { useMDXComponents as getThemeComponents } from 'nextra-theme-docs'
import { PasswordGate } from './components/PasswordGate'

const themeComponents = getThemeComponents()

export function useMDXComponents(components) {
  return {
    ...themeComponents,
    PasswordGate,
    ...components
  }
}


