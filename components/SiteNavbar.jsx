'use client'

import { useState, useEffect } from 'react'

export function SiteNavbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem',
      transition: 'all 0.3s ease',
    }}>
      {/* Logo mark */}
      <div style={{
        width: '32px',
        height: '32px',
        borderRadius: '8px',
        background: 'linear-gradient(135deg, #4f8ef7 0%, #7c6af5 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: '0 0 16px rgba(79,142,247,0.4)',
        flexShrink: 0,
        animation: 'pulse-glow 3s ease-in-out infinite',
      }}>
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7L12 2Z" fill="white" fillOpacity="0.9"/>
          <path d="M9 12l2 2 4-4" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>

      {/* Wordmark */}
      <span style={{
        fontSize: '1.05rem',
        fontWeight: '700',
        letterSpacing: '-0.025em',
        background: 'linear-gradient(135deg, #f0f2ff 0%, #4f8ef7 60%, #7c6af5 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        fontFamily: "'Inter', sans-serif",
      }}>
        PrepSuite
      </span>

      {/* Beta badge */}
      <span style={{
        fontSize: '0.6rem',
        fontWeight: '700',
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
        color: '#7c6af5',
        border: '1px solid rgba(124,106,245,0.4)',
        padding: '0.15rem 0.4rem',
        borderRadius: '4px',
        background: 'rgba(124,106,245,0.1)',
        lineHeight: 1,
      }}>
        BETA
      </span>
    </div>
  )
}
